float objectDist0(vec3 position) {
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return min(sphere, box);
}

float objectDist1(vec3 position) {
    position.x -= 5;
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return max(sphere, box);
}

float objectDist2(vec3 position) {
    position.xz -= vec2(10, 2);
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return max(sphere, -box);
}

float objectDist3(vec3 position) {
    position.xz -= vec2(10, -2);
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return max(-sphere, box);
}

float objectDist4(vec3 position) {
    position.x -= 15;
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return fOpUnionRound(sphere, box, abs(sin(time)));
}

float objectDist5(vec3 position) {
    position.x -= 20;
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return fOpUnionColumns(sphere, box, 0.1, 10);
}

float objectDist6(vec3 position) {
    position.x -= 25;
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return fOpUnionStairs(sphere, box, 0.4, 10);
}

float objectDist7(vec3 position) {
    position.xz -= vec2(30, 2);
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return fOpEngrave(sphere, box, 0.01);
}

float objectDist8(vec3 position) {
    position.xz -= vec2(30, -2);
    float sphere = fSphere(position, 1.3);
    float box = fBox(position, vec3(1));
    return fOpEngrave(box, sphere, 0.01);
}

float map(vec3 position) {
    float result = objectDist0(position);
    result = min(result, objectDist1(position));
    result = min(result, objectDist2(position));
    result = min(result, objectDist3(position));
    result = min(result, objectDist4(position));
    result = min(result, objectDist5(position));
    result = min(result, objectDist6(position));
    result = min(result, objectDist7(position));
    result = min(result, objectDist8(position));
    return result;
}

float map_iD(vec3 position) {
    float dist = objectDist0(position);
    float iD = 0;
    {
         float dist_ = objectDist1(position);
         if (dist_ < dist) dist = dist_, iD = 1;
    }
    {
         float dist_ = objectDist2(position);
         if (dist_ < dist) dist = dist_, iD = 2;
    }
    {
         float dist_ = objectDist3(position);
         if (dist_ < dist) dist = dist_, iD = 3;
    }
    {
         float dist_ = objectDist4(position);
         if (dist_ < dist) dist = dist_, iD = 4;
    }
    {
         float dist_ = objectDist5(position);
         if (dist_ < dist) dist = dist_, iD = 5;
    }
    {
         float dist_ = objectDist6(position);
         if (dist_ < dist) dist = dist_, iD = 6;
    }
    {
         float dist_ = objectDist7(position);
         if (dist_ < dist) dist = dist_, iD = 7;
    }
    {
         float dist_ = objectDist8(position);
         if (dist_ < dist) dist = dist_, iD = 8;
    }
    return iD;
}
