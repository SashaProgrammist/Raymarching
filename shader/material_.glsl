vec3 objectDistColor0(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor1(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor2(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor3(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor4(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor5(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor6(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor7(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 objectDistColor8(vec3 rayPosition, vec3 normal, vec3 rayDerection) {
    return vec3(0.4, 0.8, 0.7);
}

vec3 getMaterial(vec3 rayPosition, float id, vec3 normal, vec3 rayDerection) {
    vec3 material = vec3(0.);
    switch (int(id)) {
       case 0:
           material = objectDistColor0(rayPosition, normal, rayDerection);
           break;
       case 1:
           material = objectDistColor1(rayPosition, normal, rayDerection);
           break;
       case 2:
           material = objectDistColor2(rayPosition, normal, rayDerection);
           break;
       case 3:
           material = objectDistColor3(rayPosition, normal, rayDerection);
           break;
       case 4:
           material = objectDistColor4(rayPosition, normal, rayDerection);
           break;
       case 5:
           material = objectDistColor5(rayPosition, normal, rayDerection);
           break;
       case 6:
           material = objectDistColor6(rayPosition, normal, rayDerection);
           break;
       case 7:
           material = objectDistColor7(rayPosition, normal, rayDerection);
           break;
       case 8:
           material = objectDistColor8(rayPosition, normal, rayDerection);
           break;
        }
    return material;
}

