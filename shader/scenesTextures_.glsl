uniform sampler2D s1;
uniform sampler2D s2;
uniform sampler2D s3;
uniform sampler2D s4;
uniform sampler2D s5;
uniform sampler2D s6;
uniform sampler2D s7;
uniform sampler2D s8;
uniform sampler2D s9;
uniform sampler2D s10;
uniform sampler2D s11;
uniform sampler2D s12;
uniform sampler2D s13;
uniform sampler2D s14;
uniform sampler2D s15;
uniform sampler2D s16;
uniform sampler2D s17;
uniform sampler2D s18;
uniform sampler2D textureNotScenes;

vec3 getIconScene(int ID, vec2 uv) {
    switch (ID) {
        case 1:
        return texture(s1, uv).rgb;
        case 2:
        return texture(s2, uv).rgb;
        case 3:
        return texture(s3, uv).rgb;
        case 4:
        return texture(s4, uv).rgb;
        case 5:
        return texture(s5, uv).rgb;
        case 6:
        return texture(s6, uv).rgb;
        case 7:
        return texture(s7, uv).rgb;
        case 8:
        return texture(s8, uv).rgb;
        case 9:
        return texture(s9, uv).rgb;
        case 10:
        return texture(s10, uv).rgb;
        case 11:
        return texture(s11, uv).rgb;
        case 12:
        return texture(s12, uv).rgb;
        case 13:
        return texture(s13, uv).rgb;
        case 14:
        return texture(s14, uv).rgb;
        case 15:
        return texture(s15, uv).rgb;
        case 16:
        return texture(s16, uv).rgb;
        case 17:
        return texture(s17, uv).rgb;
        case 18:
        return texture(s18, uv).rgb;
        default:
        return texture(textureNotScenes, uv).rgb;
    }
}
