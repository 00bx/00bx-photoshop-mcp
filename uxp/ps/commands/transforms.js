/* MIT License - Copyright (c) 2025 Mike Chambers / 00bx expansion */

const { app, action } = require("photoshop");

const {
    findLayer,
    execute,
    selectLayer
} = require("./utils");

const freeTransform = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`freeTransform : Could not find layerId : ${layerId}`);
    }

    let width = options.width !== undefined ? options.width : 100;
    let height = options.height !== undefined ? options.height : 100;
    let angle = options.angle !== undefined ? options.angle : 0;
    let skewX = options.skewX !== undefined ? options.skewX : 0;
    let skewY = options.skewY !== undefined ? options.skewY : 0;
    let moveX = options.moveX !== undefined ? options.moveX : 0;
    let moveY = options.moveY !== undefined ? options.moveY : 0;

    await execute(async () => {
        selectLayer(layer, true);

        let desc = {
            _obj: "transform",
            _target: [
                {
                    _enum: "ordinal",
                    _ref: "layer",
                    _value: "targetEnum",
                },
            ],
            freeTransformCenterState: {
                _enum: "quadCenterState",
                _value: "QCSAverage",
            },
            width: {
                _unit: "percentUnit",
                _value: width,
            },
            height: {
                _unit: "percentUnit",
                _value: height,
            },
            angle: {
                _unit: "angleUnit",
                _value: angle,
            },
            skew: {
                _obj: "paint",
                horizontal: {
                    _unit: "angleUnit",
                    _value: skewX,
                },
                vertical: {
                    _unit: "angleUnit",
                    _value: skewY,
                },
            },
            offset: {
                _obj: "offset",
                horizontal: {
                    _unit: "pixelsUnit",
                    _value: moveX,
                },
                vertical: {
                    _unit: "pixelsUnit",
                    _value: moveY,
                },
            },
            interfaceIconFrameDimmed: {
                _enum: "interpolationType",
                _value: "bicubicAutomatic",
            },
        };

        await action.batchPlay([desc], {});
    });
};

const perspectiveTransform = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`perspectiveTransform : Could not find layerId : ${layerId}`);
    }

    // Four corner points: topLeft, topRight, bottomRight, bottomLeft
    // Each is {x, y} in percentage of layer bounds
    let tl = options.topLeft || { x: 0, y: 0 };
    let tr = options.topRight || { x: 100, y: 0 };
    let br = options.bottomRight || { x: 100, y: 100 };
    let bl = options.bottomLeft || { x: 0, y: 100 };

    await execute(async () => {
        selectLayer(layer, true);

        let bounds = layer.bounds;
        let w = bounds.right - bounds.left;
        let h = bounds.bottom - bounds.top;

        let commands = [{
            _obj: "transform",
            _target: [
                {
                    _enum: "ordinal",
                    _ref: "layer",
                    _value: "targetEnum",
                },
            ],
            freeTransformCenterState: {
                _enum: "quadCenterState",
                _value: "QCSAverage",
            },
            rectangle: {
                _obj: "rectangle",
                top: { _unit: "pixelsUnit", _value: bounds.top + (tl.y / 100) * h },
                left: { _unit: "pixelsUnit", _value: bounds.left + (tl.x / 100) * w },
                bottom: { _unit: "pixelsUnit", _value: bounds.top + (bl.y / 100) * h },
                right: { _unit: "pixelsUnit", _value: bounds.left + (tr.x / 100) * w },
            },
            interfaceIconFrameDimmed: {
                _enum: "interpolationType",
                _value: "bicubicAutomatic",
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const warpTransform = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`warpTransform : Could not find layerId : ${layerId}`);
    }

    let warpStyle = options.warpStyle || "arc";
    let bend = options.bend !== undefined ? options.bend : 50;
    let horizontalDistortion = options.horizontalDistortion !== undefined ? options.horizontalDistortion : 0;
    let verticalDistortion = options.verticalDistortion !== undefined ? options.verticalDistortion : 0;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "transform",
            _target: [
                {
                    _enum: "ordinal",
                    _ref: "layer",
                    _value: "targetEnum",
                },
            ],
            freeTransformCenterState: {
                _enum: "quadCenterState",
                _value: "QCSAverage",
            },
            warp: {
                _obj: "warp",
                warpStyle: {
                    _enum: "warpStyle",
                    _value: warpStyle,
                },
                warpValue: bend,
                warpPerspective: 0,
                warpPerspectiveOther: 0,
                warpRotate: {
                    _enum: "orientation",
                    _value: "horizontal",
                },
            },
            interfaceIconFrameDimmed: {
                _enum: "interpolationType",
                _value: "bicubicAutomatic",
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const contentAwareScale = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`contentAwareScale : Could not find layerId : ${layerId}`);
    }

    let width = options.width !== undefined ? options.width : 100;
    let height = options.height !== undefined ? options.height : 100;

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "contentAwareScale",
            _target: [
                {
                    _enum: "ordinal",
                    _ref: "layer",
                    _value: "targetEnum",
                },
            ],
            freeTransformCenterState: {
                _enum: "quadCenterState",
                _value: "QCSAverage",
            },
            width: {
                _unit: "percentUnit",
                _value: width,
            },
            height: {
                _unit: "percentUnit",
                _value: height,
            },
            interfaceIconFrameDimmed: {
                _enum: "interpolationType",
                _value: "bicubicAutomatic",
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const convertToSmartObject = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`convertToSmartObject : Could not find layerId : ${layerId}`);
    }

    await execute(async () => {
        selectLayer(layer, true);

        let commands = [{
            _obj: "newPlacedLayer",
        }];

        await action.batchPlay(commands, {});
    });
};

const commandHandlers = {
    freeTransform,
    perspectiveTransform,
    warpTransform,
    contentAwareScale,
    convertToSmartObject,
};

module.exports = {
    commandHandlers
};
