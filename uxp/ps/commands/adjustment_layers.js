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

const addAdjustmentLayerBlackAndWhite = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addAdjustmentLayerBlackAndWhite : Could not find layerId : ${layerId}`
        );
    }

    let colors = options.colors;
    let tintColor = options.tintColor

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "blackAndWhite",
                        blue: colors.blue,
                        cyan: colors.cyan,
                        grain: colors.green,
                        magenta: colors.magenta,
                        presetKind: {
                            _enum: "presetKindType",
                            _value: "presetKindDefault",
                        },
                        red: colors.red,
                        tintColor: {
                            _obj: "RGBColor",
                            blue: tintColor.blue,
                            grain: tintColor.green,
                            red: tintColor.red,
                        },
                        useTint: options.tint,
                        yellow: colors.yellow,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addBrightnessContrastAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addBrightnessContrastAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "brightnessEvent",
                        useLegacy: false,
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "brightnessEvent",
                    brightness: options.brightness,
                    center: options.contrast,
                    useLegacy: false,
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addAdjustmentLayerVibrance = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addAdjustmentLayerVibrance : Could not find layerId : ${layerId}`
        );
    }

    let colors = options.colors;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _class: "vibrance",
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "vibrance",
                    saturation: options.saturation,
                    vibrance: options.vibrance,
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addColorBalanceAdjustmentLayer = async (command) => {

    let options = command.options;

    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addColorBalanceAdjustmentLayer : Could not find layer named : [${layerId}]`
        );
    }

    await execute(async () => {
        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "colorBalance",
                        highlightLevels: [0, 0, 0],
                        midtoneLevels: [0, 0, 0],
                        preserveLuminosity: true,
                        shadowLevels: [0, 0, 0],
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "colorBalance",
                    highlightLevels: options.highlights,
                    midtoneLevels: options.midtones,
                    shadowLevels: options.shadows,
                },
            },
        ];
        await action.batchPlay(commands, {});
    });
};

const addCurvesAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addCurvesAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let channel = options.channel || "composite";
    let points = options.points || [{ input: 0, output: 0 }, { input: 255, output: 255 }];

    let pointsArray = points.map((p) => ({
        _obj: "paint",
        horizontal: p.input,
        vertical: p.output,
    }));

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "curves",
                        presetKind: {
                            _enum: "presetKindType",
                            _value: "presetKindCustom",
                        },
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "curves",
                    adjustment: [
                        {
                            _obj: "curvesAdjustment",
                            channel: {
                                _enum: "channel",
                                _value: channel,
                            },
                            curve: pointsArray,
                        },
                    ],
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addLevelsAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addLevelsAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let channel = options.channel || "composite";
    let inputShadow = options.inputShadow !== undefined ? options.inputShadow : 0;
    let inputHighlight = options.inputHighlight !== undefined ? options.inputHighlight : 255;
    let inputMidtone = options.inputMidtone !== undefined ? options.inputMidtone : 1.0;
    let outputShadow = options.outputShadow !== undefined ? options.outputShadow : 0;
    let outputHighlight = options.outputHighlight !== undefined ? options.outputHighlight : 255;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "levels",
                        presetKind: {
                            _enum: "presetKindType",
                            _value: "presetKindDefault",
                        },
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "levels",
                    adjustment: [
                        {
                            _obj: "levelsAdjustment",
                            channel: {
                                _enum: "channel",
                                _value: channel,
                            },
                            gamma: inputMidtone,
                            input: [inputShadow, inputHighlight],
                            output: [outputShadow, outputHighlight],
                        },
                    ],
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addHueSaturationAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addHueSaturationAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let hue = options.hue !== undefined ? options.hue : 0;
    let saturation = options.saturation !== undefined ? options.saturation : 0;
    let lightness = options.lightness !== undefined ? options.lightness : 0;
    let colorize = options.colorize !== undefined ? options.colorize : false;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "hueSaturation",
                        presetKind: {
                            _enum: "presetKindType",
                            _value: "presetKindDefault",
                        },
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "hueSaturation",
                    adjustment: [
                        {
                            _obj: "hueSatAdjustmentV2",
                            hue: hue,
                            saturation: saturation,
                            lightness: lightness,
                        },
                    ],
                    colorize: colorize,
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addPhotoFilterAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addPhotoFilterAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let color = options.color || { red: 236, green: 138, blue: 0 };
    let density = options.density !== undefined ? options.density : 25;
    let preserveLuminosity = options.preserveLuminosity !== undefined ? options.preserveLuminosity : true;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "photoFilter",
                        color: {
                            _obj: "RGBColor",
                            red: color.red,
                            grain: color.green,
                            blue: color.blue,
                        },
                        density: density,
                        preserveLuminosity: preserveLuminosity,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addChannelMixerAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addChannelMixerAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let outputChannel = options.outputChannel || "red";
    let red = options.red !== undefined ? options.red : 100;
    let green = options.green !== undefined ? options.green : 0;
    let blue = options.blue !== undefined ? options.blue : 0;
    let constant = options.constant !== undefined ? options.constant : 0;
    let monochrome = options.monochrome !== undefined ? options.monochrome : false;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "channelMixer",
                        monochromatic: monochrome,
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "channelMixer",
                    outputChannel: {
                        _enum: "channel",
                        _value: outputChannel,
                    },
                    red: red,
                    grain: green,
                    blue: blue,
                    constant: constant,
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addGradientMapAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addGradientMapAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let colorStops = options.colorStops || [
        { location: 0, color: { red: 0, green: 0, blue: 0 }, midpoint: 50 },
        { location: 100, color: { red: 255, green: 255, blue: 255 }, midpoint: 50 },
    ];
    let reverse = options.reverse !== undefined ? options.reverse : false;

    let colorStopsArray = colorStops.map((stop) => ({
        _obj: "colorStop",
        color: {
            _obj: "RGBColor",
            red: stop.color.red,
            grain: stop.color.green,
            blue: stop.color.blue,
        },
        location: Math.round(stop.location * 4096 / 100),
        midpoint: stop.midpoint !== undefined ? stop.midpoint : 50,
        type: {
            _enum: "colorStopType",
            _value: "userStop",
        },
    }));

    let opacityStopsArray = colorStops.map((stop) => ({
        _obj: "transferSpec",
        location: Math.round(stop.location * 4096 / 100),
        midpoint: 50,
        opacity: {
            _unit: "percentUnit",
            _value: 100,
        },
    }));

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "gradientMapClass",
                        gradient: {
                            _obj: "gradientClassEvent",
                            colors: colorStopsArray,
                            gradientForm: {
                                _enum: "gradientForm",
                                _value: "customStops",
                            },
                            interfaceIconFrameDimmed: 4096.0,
                            transparency: opacityStopsArray,
                        },
                        reverse: reverse,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addPosterizeAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addPosterizeAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let levels = options.levels !== undefined ? options.levels : 4;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "posterize",
                        levels: levels,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addThresholdAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addThresholdAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let level = options.level !== undefined ? options.level : 128;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "threshold",
                        level: level,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addSelectiveColorAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addSelectiveColorAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let colors = options.colors || "reds";
    let cyan = options.cyan !== undefined ? options.cyan : 0;
    let magenta = options.magenta !== undefined ? options.magenta : 0;
    let yellow = options.yellow !== undefined ? options.yellow : 0;
    let black = options.black !== undefined ? options.black : 0;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "selectiveColor",
                    },
                },
            },
            // Set current adjustment layer
            {
                _obj: "set",
                _target: [
                    {
                        _enum: "ordinal",
                        _ref: "adjustmentLayer",
                        _value: "targetEnum",
                    },
                ],
                to: {
                    _obj: "selectiveColor",
                    colorCorrection: [
                        {
                            _obj: "colorCorrection",
                            colors: {
                                _enum: "colors",
                                _value: colors,
                            },
                            cyan: cyan,
                            magenta: magenta,
                            yellowColor: yellow,
                            black: black,
                        },
                    ],
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addExposureAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addExposureAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    let exposure = options.exposure !== undefined ? options.exposure : 0;
    let offset = options.offset !== undefined ? options.offset : 0;
    let gamma = options.gamma !== undefined ? options.gamma : 1.0;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "exposure",
                        exposure: exposure,
                        offset: offset,
                        gammaCorrection: gamma,
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addInvertAdjustmentLayer = async (command) => {

    let options = command.options;
    let layerId = options.layerId;

    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(
            `addInvertAdjustmentLayer : Could not find layerId : ${layerId}`
        );
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [
            // Make adjustment layer
            {
                _obj: "make",
                _target: [
                    {
                        _ref: "adjustmentLayer",
                    },
                ],
                using: {
                    _obj: "adjustmentLayer",
                    type: {
                        _obj: "invert",
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const addSolidColorFillLayer = async (command) => {

    let options = command.options;
    let color = options.color || { red: 255, green: 0, blue: 0 };

    await execute(async () => {
        let commands = [
            // Make content layer
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
                        _obj: "solidColorLayer",
                        color: {
                            _obj: "RGBColor",
                            red: color.red,
                            grain: color.green,
                            blue: color.blue,
                        },
                    },
                },
            },
        ];

        await action.batchPlay(commands, {});
    });
};

const commandHandlers = {
    addAdjustmentLayerBlackAndWhite,
    addBrightnessContrastAdjustmentLayer,
    addAdjustmentLayerVibrance,
    addColorBalanceAdjustmentLayer,
    addCurvesAdjustmentLayer,
    addLevelsAdjustmentLayer,
    addHueSaturationAdjustmentLayer,
    addPhotoFilterAdjustmentLayer,
    addChannelMixerAdjustmentLayer,
    addGradientMapAdjustmentLayer,
    addPosterizeAdjustmentLayer,
    addThresholdAdjustmentLayer,
    addSelectiveColorAdjustmentLayer,
    addExposureAdjustmentLayer,
    addInvertAdjustmentLayer,
    addSolidColorFillLayer
}

module.exports = {
    commandHandlers
};
