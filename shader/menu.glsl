void cutMenu(inout vec3 color) {
    float e = 0.003;
    vec2 UV = getUV(vec2(0));
    float radiusBoxSetting = 0.1;
    vec2 settingShift = vec2(-0.5 * resolution.x / resolution.y, 0);
    float distBoxSetting = - radiusBoxSetting + \
                           fBox2(UV - settingShift, \
                                 vec2(0.5 - radiusBoxSetting, 0.9 - radiusBoxSetting));

    if (distBoxSetting < e) {
        float smus = getSmus(distBoxSetting / e);
        float mixBoxSetting = mix(0.5, 1.0, smus);
        color = mixBoxSetting * color;

        vec2 boxSliderShift = vec2(0.4, 0) + settingShift;
        float radiusBoxSlider = 0.05;
        float distBoxSlider = fBox2(UV - boxSliderShift, \
                                    vec2(0.05 - radiusBoxSlider, 0.8 - radiusBoxSlider)) - \
                              radiusBoxSlider;
        if (distBoxSlider < e) {
            smus = getSmus(distBoxSlider / e);
            color = mix(vec3(0.1), color, smus);

            vec2 sliderShift = vec2(0, 1.4 * positionSlider - 0.7) + boxSliderShift;
            float distSlider = fBox2(UV - sliderShift, \
                                     vec2(0.05 - radiusBoxSlider, 0.08 - radiusBoxSlider)) - \
                               radiusBoxSlider;

            if (distSlider < e) {
                smus = getSmus(distSlider / e);
                vec3 colorSlider = vec3(0.5) * \
                                   mix((sin((UV.y - sliderShift.y) * 300) + 1) / 4 + 0.5, 1, \
                                       getSmus((distSlider + 0.01) / (e + 0.01)));
                color = mix(colorSlider, color, smus);
            }
        }

        vec2 boxScenesShift = vec2(-0.1, 0) + settingShift;
        float radiusBoxScenes = 0.08;
        float distBoxScenes = fBox2(UV - boxScenesShift, \
                                    vec2(0.35 - radiusBoxScenes, 0.8 - radiusBoxScenes)) - \
                              radiusBoxScenes;
        if (distBoxScenes < e) {
            smus = getSmus(distBoxScenes / e);
            float mixBoxScenes = mix(0.8, 1.0, smus);
            color = mixBoxScenes * color;

            float radiusBoxScene = 0.02;
            for (int i; i < countsScenes; i++) {
                vec2 boxSceneShift = vec2(0, 0.65 - \
                                          i * 0.25 + \
                                          0.25 * (1 - positionSlider) * \
                                          max(countsScenes - 6, 0)) + \
                                          boxScenesShift;
                if (abs(boxSceneShift.y) >= 1) \
                        continue;
                float distBoxScene = fBox2(UV - boxSceneShift, \
                                           vec2(0.3 - radiusBoxScene, 0.1 - radiusBoxScene)) - \
                                           radiusBoxScene;
                if (distBoxScene < e) {
                    vec2 UV_Scene = UV - boxSceneShift + vec2(0.3, 0.1);
                    UV_Scene /= vec2(0.6, 0.2);
                    vec3 colorScene = getIconScene(i + 1, UV_Scene);

                    smus = 1 - getSmus(distBoxScene / e);
                    smus *= 1 - getSmus((abs(UV.y) - 0.8 + radiusBoxScenes * 1.5) / \
                                            radiusBoxScenes / 1.5);

                    float distMouseBoxScene = \
                            fBox2(mousePos - boxSceneShift, \
                                  vec2(0.3 - radiusBoxScene, 0.1 - radiusBoxScene)) - \
                                  radiusBoxScene;
                    color = mix(color, colorScene, smus);
                    if (distMouseBoxScene < e) {
                        smus = (1 - getSmus(distBoxScene / e)) * smus * 0.5;

                        color = mix(color, vec3(0.8), smus);
                    }
                }
            }
        }
    }

    settingShift = vec2(0.5 * resolution.x / resolution.y, 0);
    distBoxSetting = - radiusBoxSetting + \
                     fBox2(UV - settingShift, \
                           vec2(0.5 - radiusBoxSetting, 0.9 - radiusBoxSetting));

    if (distBoxSetting < e) {
        float smus = getSmus(distBoxSetting / e);
        float mixBoxSetting = mix(0.5, 1.0, smus);
        color = mixBoxSetting * color;
    }

    float distMouse = length(UV - mousePos) - 0.07;
    if (distMouse < e) {
        float smus = getSmus(distMouse / e);
        color +=  (1 - smus) * vec3(0.25);
    }
}
