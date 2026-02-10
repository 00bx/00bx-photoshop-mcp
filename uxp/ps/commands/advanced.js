/* MIT License - Copyright (c) 2025 Mike Chambers / 00bx expansion */

const { app, action } = require("photoshop");

const {
    findLayer,
    execute,
    selectLayer,
    hasActiveSelection
} = require("./utils");

const contentAwareFill = async (command) => {
    let options = command.options;

    if (!hasActiveSelection()) {
        throw new Error("contentAwareFill : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "fill",
            using: {
                _enum: "fillContents",
                _value: "contentAware",
            },
            opacity: {
                _unit: "percentUnit",
                _value: 100,
            },
            mode: {
                _enum: "blendMode",
                _value: "normal",
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const autoTone = async (command) => {
    await execute(async () => {
        let commands = [{
            _obj: "autoTone",
        }];
        await action.batchPlay(commands, {});
    });
};

const autoColor = async (command) => {
    await execute(async () => {
        let commands = [{
            _obj: "autoColor",
        }];
        await action.batchPlay(commands, {});
    });
};

const autoContrast = async (command) => {
    await execute(async () => {
        let commands = [{
            _obj: "autoContrast",
        }];
        await action.batchPlay(commands, {});
    });
};

const shadowsHighlights = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`shadowsHighlights : Could not find layerId : ${layerId}`);
    }

    let shadowAmount = options.shadowAmount !== undefined ? options.shadowAmount : 35;
    let shadowTonalWidth = options.shadowTonalWidth !== undefined ? options.shadowTonalWidth : 50;
    let shadowRadius = options.shadowRadius !== undefined ? options.shadowRadius : 30;
    let highlightAmount = options.highlightAmount !== undefined ? options.highlightAmount : 0;
    let highlightTonalWidth = options.highlightTonalWidth !== undefined ? options.highlightTonalWidth : 50;
    let highlightRadius = options.highlightRadius !== undefined ? options.highlightRadius : 30;
    let colorCorrection = options.colorCorrection !== undefined ? options.colorCorrection : 20;
    let midtoneContrast = options.midtoneContrast !== undefined ? options.midtoneContrast : 0;
    let blackClip = options.blackClip !== undefined ? options.blackClip : 0.01;
    let whiteClip = options.whiteClip !== undefined ? options.whiteClip : 0.01;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "shadowHighlight",
            shadowAmount: {
                _unit: "percentUnit",
                _value: shadowAmount,
            },
            shadowWidth: {
                _unit: "percentUnit",
                _value: shadowTonalWidth,
            },
            shadowRadiusPixels: shadowRadius,
            highlightAmount: {
                _unit: "percentUnit",
                _value: highlightAmount,
            },
            highlightWidth: {
                _unit: "percentUnit",
                _value: highlightTonalWidth,
            },
            highlightRadiusPixels: highlightRadius,
            colorCorrection: colorCorrection,
            midtoneContrast: midtoneContrast,
            blackClip: {
                _unit: "percentUnit",
                _value: blackClip,
            },
            whiteClip: {
                _unit: "percentUnit",
                _value: whiteClip,
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const lensCorrection = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`lensCorrection : Could not find layerId : ${layerId}`);
    }

    let distortion = options.distortion !== undefined ? options.distortion : 0;
    let vignette = options.vignette !== undefined ? options.vignette : 0;
    let vignetteMidpoint = options.vignetteMidpoint !== undefined ? options.vignetteMidpoint : 50;
    let chromaticAberrationRG = options.chromaticAberrationRG !== undefined ? options.chromaticAberrationRG : 0;
    let chromaticAberrationBY = options.chromaticAberrationBY !== undefined ? options.chromaticAberrationBY : 0;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "newLensCorrection",
            lensManualDistortion: distortion,
            lensManualChromaticAberrationRC: chromaticAberrationRG,
            lensManualChromaticAberrationBY: chromaticAberrationBY,
            lensManualVignette: vignette,
            lensManualVignetteMidpoint: vignetteMidpoint,
        }];

        await action.batchPlay(commands, {});
    });
};

const liquifyForward = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`liquifyForward : Could not find layerId : ${layerId}`);
    }

    let startX = options.startX || 100;
    let startY = options.startY || 100;
    let endX = options.endX || 150;
    let endY = options.endY || 100;
    let brushSize = options.brushSize || 64;
    let pressure = options.pressure || 50;

    await execute(async () => {
        selectLayer(layer, true);

        // Liquify uses the "plastic" filter with mesh data
        // Simplified: use displacement map approach via batchPlay
        let commands = [{
            _obj: "liquify",
            liquifyMesh: {
                _obj: "liquifyMesh",
            },
        }];

        // Note: Full programmatic liquify requires mesh manipulation
        // which is extremely complex. This is a stub that opens
        // the liquify dialog. For programmatic displacement, use
        // the displace filter instead.
        await action.batchPlay(commands, {});
    });
};

const applyDisplace = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`applyDisplace : Could not find layerId : ${layerId}`);
    }

    let horizontalScale = options.horizontalScale || 10;
    let verticalScale = options.verticalScale || 10;
    let stretchToFit = options.stretchToFit !== undefined ? options.stretchToFit : true;
    let wrapAround = options.wrapAround !== undefined ? options.wrapAround : true;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "displace",
            horizontalScale: horizontalScale,
            verticalScale: verticalScale,
            displacementMap: {
                _enum: "displacementMap",
                _value: stretchToFit ? "stretchToFit" : "tile",
            },
            undefinedArea: {
                _enum: "undefinedArea",
                _value: wrapAround ? "wrapAround" : "repeatEdgePixels",
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const applySphere = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`applySphere : Could not find layerId : ${layerId}`);
    }

    let amount = options.amount !== undefined ? options.amount : 100;
    let mode = options.mode || "normal";

    let modeMap = {
        normal: "normal",
        horizontal: "horizontalOnly",
        vertical: "verticalOnly",
    };

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "spherize",
            amount: amount,
            mode: {
                _enum: "spherizeMode",
                _value: modeMap[mode] || "normal",
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const applyWave = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`applyWave : Could not find layerId : ${layerId}`);
    }

    let generators = options.generators || 5;
    let wavelengthMin = options.wavelengthMin || 10;
    let wavelengthMax = options.wavelengthMax || 120;
    let amplitudeMin = options.amplitudeMin || 5;
    let amplitudeMax = options.amplitudeMax || 35;
    let scale = options.scale || 100;
    let waveType = options.waveType || "sine";

    let typeMap = {
        sine: "triangular",
        triangle: "triangular",
        square: "squareWave",
    };

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "wave",
            numberOfGenerators: generators,
            minimumWavelength: wavelengthMin,
            maximumWavelength: wavelengthMax,
            minimumAmplitude: amplitudeMin,
            maximumAmplitude: amplitudeMax,
            horizontalScale: {
                _unit: "percentUnit",
                _value: scale,
            },
            verticalScale: {
                _unit: "percentUnit",
                _value: scale,
            },
            waveType: {
                _enum: "waveType",
                _value: waveType === "sine" ? "sinusoidal" : (typeMap[waveType] || "sinusoidal"),
            },
            undefinedAreas: {
                _enum: "undefinedArea",
                _value: "wrapAround",
            },
            randomSeed: Math.floor(Math.random() * 100),
        }];

        await action.batchPlay(commands, {});
    });
};

const commandHandlers = {
    contentAwareFill,
    autoTone,
    autoColor,
    autoContrast,
    shadowsHighlights,
    lensCorrection,
    liquifyForward,
    applyDisplace,
    applySphere,
    applyWave,
};

module.exports = {
    commandHandlers
};
