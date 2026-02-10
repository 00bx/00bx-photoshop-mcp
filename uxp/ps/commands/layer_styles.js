/* MIT License
 *
 * Copyright (c) 2025 Mike Chambers
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

const { action } = require("photoshop");

const {
    selectLayer,
    findLayer,
    execute
} = require("./utils")

const addDropShadowLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addDropShadowLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Set Layer Styles of current layer
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    dropShadow: {
                        _obj: "dropShadow",
                        antiAlias: false,
                        blur: {
                            _unit: "pixelsUnit",
                            _value: options.size,
                        },
                        chokeMatte: {
                            _unit: "pixelsUnit",
                            _value: options.spread,
                        },
                        color: {
                            _obj: "RGBColor",
                            blue: options.color.blue,
                            grain: options.color.green,
                            red: options.color.red,
                        },
                        distance: {
                            _unit: "pixelsUnit",
                            _value: options.distance,
                        },
                        enabled: true,
                        layerConceals: true,
                        localLightingAngle: {
                            _unit: "angleUnit",
                            _value: options.angle,
                        },
                        mode: {
                            _enum: "blendMode",
                            _value: options.blendMode.toLowerCase(),
                        },
                        noise: {
                            _unit: "percentUnit",
                            _value: 0.0,
                        },
                        opacity: {
                            _unit: "percentUnit",
                            _value: options.opacity,
                        },
                        present: true,
                        showInDialog: true,
                        transferSpec: {
                            _obj: "shapeCurveType",
                            name: "Linear",
                        },
                        useGlobalAngle: true,
                    },
                    globalLightingAngle: {
                        _unit: "angleUnit",
                        _value: options.angle,
                    },
                    scale: {
                        _unit: "percentUnit",
                        _value: 100.0,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addStrokeLayerStyle = async (command) => {
    const options = command.options

    const layerId = options.layerId

    let layer = findLayer(layerId)

    if (!layer) {
        throw new Error(
            `addStrokeLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    let position = "centeredFrame"

    if (options.position == "INSIDE") {
        position = "insetFrame"
    } else if (options.position == "OUTSIDE") {
        position = "outsetFrame"
    }


    await execute(async () => {
        selectLayer(layer, true);

        let strokeColor = options.color
        let commands = [
            // Set Layer Styles of current layer
            {
                "_obj": "set",
                "_target": [
                    {
                        "_property": "layerEffects",
                        "_ref": "property"
                    },
                    {
                        "_enum": "ordinal",
                        "_ref": "layer",
                        "_value": "targetEnum"
                    }
                ],
                "to": {
                    "_obj": "layerEffects",
                    "frameFX": {
                        "_obj": "frameFX",
                        "color": {
                            "_obj": "RGBColor",
                            "blue": strokeColor.blue,
                            "grain": strokeColor.green,
                            "red": strokeColor.red
                        },
                        "enabled": true,
                        "mode": {
                            "_enum": "blendMode",
                            "_value": options.blendMode.toLowerCase()
                        },
                        "opacity": {
                            "_unit": "percentUnit",
                            "_value": options.opacity
                        },
                        "overprint": false,
                        "paintType": {
                            "_enum": "frameFill",
                            "_value": "solidColor"
                        },
                        "present": true,
                        "showInDialog": true,
                        "size": {
                            "_unit": "pixelsUnit",
                            "_value": options.size
                        },
                        "style": {
                            "_enum": "frameStyle",
                            "_value": position
                        }
                    },
                    "scale": {
                        "_unit": "percentUnit",
                        "_value": 100.0
                    }
                }
            }
        ];

        await action.batchPlay(commands, {});
    });
}

const createGradientLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `createGradientAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let angle = options.angle;
        let colorStops = options.colorStops;
        let opacityStops = options.opacityStops;

        let colors = [];
        for (let c of colorStops) {
            colors.push({
                _obj: "colorStop",
                color: {
                    _obj: "RGBColor",
                    blue: c.color.blue,
                    grain: c.color.green,
                    red: c.color.red,
                },
                location: Math.round((c.location / 100) * 4096),
                midpoint: c.midpoint,
                type: {
                    _enum: "colorStopType",
                    _value: "userStop",
                },
            });
        }

        let opacities = [];
        for (let o of opacityStops) {
            opacities.push({
                _obj: "transferSpec",
                location: Math.round((o.location / 100) * 4096),
                midpoint: o.midpoint,
                opacity: {
                    _unit: "percentUnit",
                    _value: o.opacity,
                },
            });
        }

        let commands = [
            // Make fill layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "contentLayer",
                    },
                ],
                using: {
                    _obj: "contentLayer",
                    type: {
                        _obj: "gradientLayer",
                        angle: {
                            _unit: "angleUnit",
                            _value: angle,
                        },
                        gradient: {
                            _obj: "gradientClassEvent",
                            colors: colors,
                            gradientForm: {
                                _enum: "gradientForm",
                                _value: "customStops",
                            },
                            interfaceIconFrameDimmed: 4096.0,
                            name: "Custom",
                            transparency: opacities,
                        },
                        gradientsInterpolationMethod: {
                            _enum: "gradientInterpolationMethodType",
                            _value: "smooth",
                        },
                        type: {
                            _enum: "gradientType",
                            _value: options.type.toLowerCase(),
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addInnerShadowLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addInnerShadowLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    innerShadow: {
                        _obj: "innerShadow",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        mode: {
                            _enum: "blendMode",
                            _value: options.blendMode.toLowerCase(),
                        },
                        color: {
                            _obj: "RGBColor",
                            red: options.color.red,
                            grain: options.color.green,
                            blue: options.color.blue,
                        },
                        opacity: {
                            _unit: "percentUnit",
                            _value: options.opacity,
                        },
                        useGlobalAngle: true,
                        localLightingAngle: {
                            _unit: "angleUnit",
                            _value: options.angle,
                        },
                        distance: {
                            _unit: "pixelsUnit",
                            _value: options.distance,
                        },
                        chokeMatte: {
                            _unit: "pixelsUnit",
                            _value: options.choke,
                        },
                        blur: {
                            _unit: "pixelsUnit",
                            _value: options.size,
                        },
                        antiAlias: false,
                        noise: {
                            _unit: "percentUnit",
                            _value: 0,
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addOuterGlowLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addOuterGlowLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    outerGlow: {
                        _obj: "outerGlow",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        mode: {
                            _enum: "blendMode",
                            _value: options.blendMode.toLowerCase(),
                        },
                        color: {
                            _obj: "RGBColor",
                            red: options.color.red,
                            grain: options.color.green,
                            blue: options.color.blue,
                        },
                        opacity: {
                            _unit: "percentUnit",
                            _value: options.opacity,
                        },
                        chokeMatte: {
                            _unit: "pixelsUnit",
                            _value: options.spread,
                        },
                        blur: {
                            _unit: "pixelsUnit",
                            _value: options.size,
                        },
                        noise: {
                            _unit: "percentUnit",
                            _value: options.noise,
                        },
                        antiAlias: false,
                        transferSpec: {
                            _obj: "shapeCurveType",
                            name: "Linear",
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addInnerGlowLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addInnerGlowLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    let sourceVal = "edgeGlow";
    if (options.source && options.source.toLowerCase() === "center") {
        sourceVal = "centerGlow";
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    innerGlow: {
                        _obj: "innerGlow",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        mode: {
                            _enum: "blendMode",
                            _value: options.blendMode.toLowerCase(),
                        },
                        color: {
                            _obj: "RGBColor",
                            red: options.color.red,
                            grain: options.color.green,
                            blue: options.color.blue,
                        },
                        opacity: {
                            _unit: "percentUnit",
                            _value: options.opacity,
                        },
                        glowTechnique: {
                            _enum: "matteTechnique",
                            _value: "softMatte",
                        },
                        chokeMatte: {
                            _unit: "pixelsUnit",
                            _value: options.choke,
                        },
                        blur: {
                            _unit: "pixelsUnit",
                            _value: options.size,
                        },
                        noise: {
                            _unit: "percentUnit",
                            _value: options.noise,
                        },
                        innerGlowSource: {
                            _enum: "innerGlowSourceType",
                            _value: sourceVal,
                        },
                        antiAlias: false,
                        transferSpec: {
                            _obj: "shapeCurveType",
                            name: "Linear",
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addBevelEmbossLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addBevelEmbossLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    let directionVal = "stampIn";
    if (options.direction && options.direction.toLowerCase() === "down") {
        directionVal = "stampOut";
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    bevelEmboss: {
                        _obj: "bevelEmboss",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        style: {
                            _enum: "bevelEmbossStyle",
                            _value: options.style,
                        },
                        technique: {
                            _enum: "bevelTechnique",
                            _value: options.technique,
                        },
                        strength: {
                            _unit: "percentUnit",
                            _value: options.depth,
                        },
                        bevelDirection: {
                            _enum: "bevelEmbossStampStyle",
                            _value: directionVal,
                        },
                        blur: {
                            _unit: "pixelsUnit",
                            _value: options.size,
                        },
                        softness: {
                            _unit: "pixelsUnit",
                            _value: options.soften,
                        },
                        localLightingAngle: {
                            _unit: "angleUnit",
                            _value: options.angle,
                        },
                        localLightingAltitude: {
                            _unit: "angleUnit",
                            _value: options.altitude,
                        },
                        useGlobalAngle: false,
                        highlightMode: {
                            _enum: "blendMode",
                            _value: options.highlightMode.toLowerCase(),
                        },
                        highlightColor: {
                            _obj: "RGBColor",
                            red: options.highlightColor.red,
                            grain: options.highlightColor.green,
                            blue: options.highlightColor.blue,
                        },
                        highlightOpacity: {
                            _unit: "percentUnit",
                            _value: options.highlightOpacity,
                        },
                        shadowMode: {
                            _enum: "blendMode",
                            _value: options.shadowMode.toLowerCase(),
                        },
                        shadowColor: {
                            _obj: "RGBColor",
                            red: options.shadowColor.red,
                            grain: options.shadowColor.green,
                            blue: options.shadowColor.blue,
                        },
                        shadowOpacity: {
                            _unit: "percentUnit",
                            _value: options.shadowOpacity,
                        },
                        antialiasGloss: false,
                        transferSpec: {
                            _obj: "shapeCurveType",
                            name: "Linear",
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addSatinLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addSatinLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    chromeFX: {
                        _obj: "chromeFX",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        mode: {
                            _enum: "blendMode",
                            _value: options.blendMode.toLowerCase(),
                        },
                        color: {
                            _obj: "RGBColor",
                            red: options.color.red,
                            grain: options.color.green,
                            blue: options.color.blue,
                        },
                        antiAlias: true,
                        invert: options.invert,
                        opacity: {
                            _unit: "percentUnit",
                            _value: options.opacity,
                        },
                        localLightingAngle: {
                            _unit: "angleUnit",
                            _value: options.angle,
                        },
                        distance: {
                            _unit: "pixelsUnit",
                            _value: options.distance,
                        },
                        blur: {
                            _unit: "pixelsUnit",
                            _value: options.size,
                        },
                        mappingShape: {
                            _obj: "shapeCurveType",
                            name: "Linear",
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addColorOverlayLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addColorOverlayLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    solidFill: {
                        _obj: "solidFill",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        mode: {
                            _enum: "blendMode",
                            _value: options.blendMode.toLowerCase(),
                        },
                        color: {
                            _obj: "RGBColor",
                            red: options.color.red,
                            grain: options.color.green,
                            blue: options.color.blue,
                        },
                        opacity: {
                            _unit: "percentUnit",
                            _value: options.opacity,
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addGradientOverlayLayerStyle = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addGradientOverlayLayerStyle : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let blendMode = (options.blendMode || "normal").toLowerCase();
        let opacity = options.opacity !== undefined ? options.opacity : 100;
        let angle = options.angle !== undefined ? options.angle : 90;
        let scale = options.scale !== undefined ? options.scale : 100;
        let type = (options.type || "linear").toLowerCase();
        let reverse = options.reverse !== undefined ? options.reverse : false;
        let colorStops = options.colorStops || [];
        let opacityStops = options.opacityStops || [];

        let colors = [];
        for (let c of colorStops) {
            colors.push({
                _obj: "colorStop",
                color: {
                    _obj: "RGBColor",
                    blue: c.color.blue,
                    grain: c.color.green,
                    red: c.color.red,
                },
                location: Math.round((c.location / 100) * 4096),
                midpoint: c.midpoint || 50,
                type: {
                    _enum: "colorStopType",
                    _value: "userStop",
                },
            });
        }

        let opacities = [];
        for (let o of opacityStops) {
            opacities.push({
                _obj: "transferSpec",
                location: Math.round((o.location / 100) * 4096),
                midpoint: o.midpoint || 50,
                opacity: {
                    _unit: "percentUnit",
                    _value: o.opacity !== undefined ? o.opacity : 100,
                },
            });
        }

        let commands = [
            {
                _obj: "set",
                _target: [
                    {
                        _property: "layerEffects",
                        _ref: "property",
                    },
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "layerEffects",
                    gradientFill: {
                        _obj: "gradientFill",
                        enabled: true,
                        present: true,
                        showInDialog: true,
                        mode: {
                            _enum: "blendMode",
                            _value: blendMode,
                        },
                        opacity: {
                            _unit: "percentUnit",
                            _value: opacity,
                        },
                        gradient: {
                            _obj: "gradientClassEvent",
                            colors: colors,
                            gradientForm: {
                                _enum: "gradientForm",
                                _value: "customStops",
                            },
                            interfaceIconFrameDimmed: 4096.0,
                            name: "Custom",
                            transparency: opacities,
                        },
                        angle: {
                            _unit: "angleUnit",
                            _value: angle,
                        },
                        type: {
                            _enum: "gradientType",
                            _value: type,
                        },
                        reverse: reverse,
                        align: true,
                        scale: {
                            _unit: "percentUnit",
                            _value: scale,
                        },
                        offset: {
                            _obj: "paint",
                            horizontal: {
                                _unit: "percentUnit",
                                _value: 0,
                            },
                            vertical: {
                                _unit: "percentUnit",
                                _value: 0,
                            },
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const clearLayerStyles = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `clearLayerStyles : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            {
                _obj: "clearLayerEffects",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "layer",
                        _value: "targetEnum",
                    },
                ],
            },
        ];

        await action.batchPlay(commands, {});
    });
};


const commandHandlers = {
    createGradientLayerStyle,
    addStrokeLayerStyle,
    addDropShadowLayerStyle,
    addInnerShadowLayerStyle,
    addOuterGlowLayerStyle,
    addInnerGlowLayerStyle,
    addBevelEmbossLayerStyle,
    addSatinLayerStyle,
    addColorOverlayLayerStyle,
    addGradientOverlayLayerStyle,
    clearLayerStyles
};

module.exports = {
    commandHandlers
};
