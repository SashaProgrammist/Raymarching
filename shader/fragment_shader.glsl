#version 400

#include hg_sdf.glsl

#include scenesConst_.glsl

#include textures_.glsl

out vec4 fragColor;
uniform vec2 resolution;
uniform vec3 rotation;
uniform vec3 startPosition;
uniform vec2 mousePos;
uniform float time;
uniform bool isTab;
uniform float positionSlider;
uniform int countsScenes;
uniform int maxSteps;
uniform int AA;

vec3 sunPosition = vec3(100);

float hash(vec2 p) {
    p = 50.0*fract(p*0.3183099);
    return fract(p.x*p.y*(p.x+p.y));
}

float noise(in vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f*f*(3.0-2.0*f);
    return -1.0+2.0*mix(mix(hash(i + vec2(0.0, 0.0)), \
                            hash(i + vec2(1.0, 0.0)), u.x), \
                        mix(hash(i + vec2(0.0, 1.0)), \
                            hash(i + vec2(1.0, 1.0)), u.x), u.y);
}

float getSmus(float value) {
    value = saturate(value);
    value = value * value * (3 - 2 * value);
    return value;
}

vec3 texturize(sampler2D sa, vec3 p, vec3 n, in vec3 gx, in vec3 gy) {
    vec3 x = textureGrad(sa, p.yz, gx.yz, gy.yz).xyz;
    vec3 y = textureGrad(sa, p.zx, gx.zx, gy.zx).xyz;
    vec3 z = textureGrad(sa, p.xy, gx.xy, gy.xy).xyz;

    return x*abs(n.x) + y*abs(n.y) + z*abs(n.z);
}

vec3 triPlanar(sampler2D _texture, vec3 position, vec3 normal, float scale) {
    normal = abs(normal);
    normal = normalize(pow(normal, vec3(5)));
    position = position * scale;
    vec3 result = (
    texture(_texture, position.yz) * normal.x +
    texture(_texture, position.xz) * normal.y +
    texture(_texture, position.xy) * normal.z).rgb;

    return result;
}

float bumpMapping(\
        sampler2D _texture, \
        vec3 position, vec3 normal, float dist, \
        float factor, float scale) {
    float bump = 0.0;
    normal = abs(normal);
    if (dist < PROCESSING_DISTANCE_BAMP) {
        vec3 bump3 = triPlanar(_texture, position, normal, scale);
        //vec3 bump3 = texturize(_texture, position * scale, normal, vec3(0.001), vec3(0.001));
        bump += factor * (bump3.r + bump3.g + bump3.b) / 3;
    }

    return bump;
}

mat4 rotationMat(in vec3 xyz) {
    vec3 _sin = sin(xyz);
    vec3 _cos = cos(xyz);

    return mat4(_cos.y*_cos.z, _cos.y*_sin.z, -_sin.y, 0.0,
    _sin.x*_sin.y*_cos.z-_cos.x*_sin.z, _sin.x*_sin.y*_sin.z+_cos.x*_cos.z, _sin.x*_cos.y, 0.0,
    _cos.x*_sin.y*_cos.z+_sin.x*_sin.z, _cos.x*_sin.y*_sin.z-_sin.x*_cos.z, _cos.x*_cos.y, 0.0,
    0.0, 0.0, 0.0, 1.0);
}

mat3 rotationMatrix(in vec3 xyz) {
    vec3 _sin = sin(xyz);
    vec3 _cos = cos(xyz);

    return mat3(_cos.y*_cos.z, _cos.y*_sin.z, -_sin.y,
    _sin.x*_sin.y*_cos.z-_cos.x*_sin.z, _sin.x*_sin.y*_sin.z+_cos.x*_cos.z, _sin.x*_cos.y,
    _cos.x*_sin.y*_cos.z+_sin.x*_sin.z, _cos.x*_sin.y*_sin.z-_sin.x*_cos.z, _cos.x*_cos.y);
}

mat2 rotationMatrix(in float a) {
    float _sin = sin(a);
    float _cos = cos(a);

    return mat2(_cos, -_sin, \
                _sin, _cos);
}

#include globalVariables_.glsl
#include map_.glsl
#include material_.glsl

float rayMarch(vec3 rayPosition, vec3 rayDerection) {
    float hit, object;

    for (int i = 0; i < maxSteps; i++) {
        vec3 currentRayPosition = rayPosition + object * rayDerection;
        hit = map(currentRayPosition);
        object += hit;
        if (abs(hit) < EPSILON || object > MAX_DISTANS) break;
    }
    return object;
}

vec3 getNormal(vec3 position) {
    vec2 e = vec2(EPSILON, 0.);
    vec3 n = vec3(map(position)) -
    vec3(map(position - e.xyy), map(position - e.yxy), map(position - e.yyx));
    return normalize(n);
}

float getSoftShadow(vec3 rayPosition, vec3 lightPosition) {
    vec3 lightDerection = normalize(lightPosition - rayPosition);
    float result = 1.;
    float dist = map(rayPosition);
    float lightSize = 0.1;

    if (dist < EPSILON / 100) \
        return 0;

    for (int i = 0; i < maxSteps; i++) {
        float hit = map(rayPosition + lightDerection * dist);
        result = min(result, hit / (dist * lightSize));
        dist += hit;
        if (abs(hit) < EPSILON || dist > MAX_DISTANS) {
            result = min(float(dist > MAX_DISTANS), result);
            break;
        }
    }
    return saturate(result);
}

float getAmbientOcclusion(vec3 rayPosition, vec3 normal) {
    float occ = 0.;
    float weight = 1.;

    for (int i = 0; i < 21; i++) {
        float len = 0.001 + 1 * float(i * i) / 400;
        float dist = map(rayPosition + normal * len);
        occ += (len - dist) * weight;
        weight *= 0.85;
    }

    return 1.0 - clamp(0.8 * occ, 0., 1.);
}

vec3 getLight(vec3 rayPosition, vec3 rayDerection, float id) {
    vec3 L = normalize(sunPosition - rayPosition);
    vec3 N = getNormal(rayPosition);
    vec3 V = -rayDerection;
    vec3 R = reflect(-L, N);

    vec3 color = getMaterial(rayPosition, id, N, rayDerection);

    float shadow = getSoftShadow(rayPosition + N * 0.05, sunPosition);
    float occ = getAmbientOcclusion(rayPosition, N);

    vec3 specColor = vec3(0.5);
    vec3 specular = specColor * pow(saturate(dot(R, V)), 10.);
    vec3 diffuse = color * saturate(dot(L, N));
    vec3 ambient = color * 0.10;
    vec3 fresnel = 0.15 * color * pow((1.0 - dot(rayDerection, N)) / 2, 3.);
    vec3 back = 0.05 * color * saturate(dot(N, -L));

    return saturate((back + ambient + fresnel) * occ + (diffuse + specular) * shadow * occ);
}

vec3 render(in vec2 normalizeCord) {
    vec3 color = vec3(0.);
    vec3 rayDerection = normalize(vec3(FOV, normalizeCord.x, normalizeCord.y));
    mat3 rotationMatrix = rotationMatrix(rotation);
    rayDerection = rotationMatrix * rayDerection;

    float object = rayMarch(startPosition, rayDerection);

    if (object < MAX_DISTANS) {
        vec3 rayPosition = startPosition + object * rayDerection;
        color += getLight(rayPosition, rayDerection,
        map_iD(rayPosition));

        color = mix(color, BECK_GROUND, 1.0 - exp(-0.00008 * square(object)));
    } else {
        color += BECK_GROUND - max(0.8 * rayDerection.z, 0.0);
    }

    return color;
}

vec2 getUV(vec2 offset) {
    return (2.0 * (gl_FragCoord.xy + offset) - resolution.xy) / resolution.y;
}

vec3 renderAA(int AA) {
    vec3 colorAA;
    for (int i = 0; i < AA; i++) \
        for (int j = 0; j < AA; j++) \
            colorAA += render(getUV(vec2(float(i), float(j)) / float(AA - 1) - 0.5));

    return colorAA / (AA * AA);
}

#include scenesTextures_.glsl
#include menu.glsl

void main() {
    initGlobalVariables();

    pR(sunPosition.xy, time);

    vec3 color;
    //    if (gl_FragCoord.x < (resolution.x * 0.332))
    //    color = renderAA(4);
    //    else if (gl_FragCoord.x < (resolution.x * 0.334))
    //    color = vec3(1., 0, 0);
    //    else if (gl_FragCoord.x < (resolution.x * 0.665))
    //    color = renderAA(2);
    //    else if (gl_FragCoord.x < (resolution.x * 0.667))
    //    color = vec3(1., 0, 0);
    //    else
    //    color = renderAA(1);
    if (AA > 1) \
        color = renderAA(AA);
    else \
        color = render(getUV(vec2(0)));

    if (isTab) \
        cutMenu(color);

    color = pow(color, vec3(0.4545));
    fragColor = vec4(color, 1);
}
