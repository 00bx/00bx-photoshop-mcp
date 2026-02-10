/* MIT License - Copyright (c) 2025 Mike Chambers / 00bx expansion */

const { app, action } = require("photoshop");

const {
    findLayer,
    execute,
    selectLayer
} = require("./utils");

const brushStroke = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`brushStroke : Could not find layerId : ${layerId}`);
    }

    let points = options.points || [{ x: 0, y: 0 }, { x: 100, y: 100 }];
    let brushSize = options.brushSize || 10;
    let color = options.color || { red: 255, green: 255, blue: 255 };
    let opacity = options.opacity || 100;
    let hardness = options.hardness || 100;
    let flow = options.flow || 100;

    await execute(async () => {
        selectLayer(layer, true);

        // Set foreground color
        let setColorCmd = [{
            _obj: "set",
            _target: [{ _ref: "color", _property: "foregroundColor" }],
            to: {
                _obj: "RGBColor",
                red: color.red,
                grain: color.green,
                blue: color.blue,
            },
        }];
        await action.batchPlay(setColorCmd, {});

        // Set brush tool with size
        let setBrushCmd = [{
            _obj: "set",
            _target: [{ _ref: "brush", _enum: "ordinal", _value: "targetEnum" }],
            to: {
                _obj: "brush",
                diameter: { _unit: "pixelsUnit", _value: brushSize },
                hardness: { _unit: "percentUnit", _value: hardness },
            },
        }];
        await action.batchPlay(setBrushCmd, {});

        // Build paint stroke path
        let pathPoints = points.map((p) => ({
            _obj: "paintPoint",
            horizontal: { _unit: "pixelsUnit", _value: p.x },
            vertical: { _unit: "pixelsUnit", _value: p.y },
            pressure: { _unit: "percentUnit", _value: 100 },
        }));

        let paintCmd = [{
            _obj: "paint",
            _target: [
                {
                    _enum: "ordinal",
                    _ref: "layer",
                    _value: "targetEnum",
                },
            ],
            mode: {
                _enum: "blendMode",
                _value: "normal",
            },
            opacity: {
                _unit: "percentUnit",
                _value: opacity,
            },
            flow: {
                _unit: "percentUnit",
                _value: flow,
            },
            from: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: points[0].x },
                vertical: { _unit: "pixelsUnit", _value: points[0].y },
            },
            to: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: points[points.length - 1].x },
                vertical: { _unit: "pixelsUnit", _value: points[points.length - 1].y },
            },
            strokeList: pathPoints,
        }];

        await action.batchPlay(paintCmd, {});
    });
};

const eraserStroke = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`eraserStroke : Could not find layerId : ${layerId}`);
    }

    let points = options.points || [{ x: 0, y: 0 }, { x: 100, y: 100 }];
    let brushSize = options.brushSize || 10;
    let opacity = options.opacity || 100;
    let hardness = options.hardness || 100;

    await execute(async () => {
        selectLayer(layer, true);

        // Select eraser tool
        let selectToolCmd = [{
            _obj: "select",
            _target: [{ _ref: "eraserTool" }],
        }];
        await action.batchPlay(selectToolCmd, {});

        // Set brush params
        let setBrushCmd = [{
            _obj: "set",
            _target: [{ _ref: "brush", _enum: "ordinal", _value: "targetEnum" }],
            to: {
                _obj: "brush",
                diameter: { _unit: "pixelsUnit", _value: brushSize },
                hardness: { _unit: "percentUnit", _value: hardness },
            },
        }];
        await action.batchPlay(setBrushCmd, {});

        // Build erase path
        let pathPoints = points.map((p) => ({
            _obj: "paintPoint",
            horizontal: { _unit: "pixelsUnit", _value: p.x },
            vertical: { _unit: "pixelsUnit", _value: p.y },
            pressure: { _unit: "percentUnit", _value: 100 },
        }));

        let eraseCmd = [{
            _obj: "paint",
            mode: {
                _enum: "blendMode",
                _value: "normal",
            },
            opacity: {
                _unit: "percentUnit",
                _value: opacity,
            },
            from: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: points[0].x },
                vertical: { _unit: "pixelsUnit", _value: points[0].y },
            },
            to: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: points[points.length - 1].x },
                vertical: { _unit: "pixelsUnit", _value: points[points.length - 1].y },
            },
            strokeList: pathPoints,
        }];

        await action.batchPlay(eraseCmd, {});

        // Switch back to brush tool
        let switchBackCmd = [{
            _obj: "select",
            _target: [{ _ref: "paintbrushTool" }],
        }];
        await action.batchPlay(switchBackCmd, {});
    });
};

const gradientDraw = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`gradientDraw : Could not find layerId : ${layerId}`);
    }

    let startPoint = options.startPoint || { x: 0, y: 0 };
    let endPoint = options.endPoint || { x: 100, y: 100 };
    let gradientType = options.gradientType || "linear";
    let opacity = options.opacity || 100;
    let colorStops = options.colorStops || [
        { location: 0, color: { red: 0, green: 0, blue: 0 }, midpoint: 50 },
        { location: 100, color: { red: 255, green: 255, blue: 255 }, midpoint: 50 },
    ];

    await execute(async () => {
        selectLayer(layer, true);

        let colors = colorStops.map((stop) => ({
            _obj: "colorStop",
            color: {
                _obj: "RGBColor",
                red: stop.color.red,
                grain: stop.color.green,
                blue: stop.color.blue,
            },
            location: Math.round(stop.location * 4096 / 100),
            midpoint: stop.midpoint !== undefined ? stop.midpoint : 50,
            type: { _enum: "colorStopType", _value: "userStop" },
        }));

        let opacities = colorStops.map((stop) => ({
            _obj: "transferSpec",
            location: Math.round(stop.location * 4096 / 100),
            midpoint: 50,
            opacity: { _unit: "percentUnit", _value: 100 },
        }));

        let typeMap = {
            linear: "linear",
            radial: "radial",
            angle: "angle",
            reflected: "reflected",
            diamond: "diamond",
        };

        let commands = [{
            _obj: "gradientClassEvent",
            from: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: startPoint.x },
                vertical: { _unit: "pixelsUnit", _value: startPoint.y },
            },
            to: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: endPoint.x },
                vertical: { _unit: "pixelsUnit", _value: endPoint.y },
            },
            type: {
                _enum: "gradientType",
                _value: typeMap[gradientType] || "linear",
            },
            gradient: {
                _obj: "gradientClassEvent",
                colors: colors,
                gradientForm: { _enum: "gradientForm", _value: "customStops" },
                interfaceIconFrameDimmed: 4096.0,
                name: "Custom",
                transparency: opacities,
            },
            opacity: {
                _unit: "percentUnit",
                _value: opacity,
            },
            mode: { _enum: "blendMode", _value: "normal" },
            useMask: true,
            dither: true,
        }];

        await action.batchPlay(commands, {});
    });
};

const paintBucketFill = async (command) => {
    let options = command.options;
    let layerId = options.layerId;
    let layer = findLayer(layerId);

    if (!layer) {
        throw new Error(`paintBucketFill : Could not find layerId : ${layerId}`);
    }

    let x = options.x || 0;
    let y = options.y || 0;
    let color = options.color || { red: 255, green: 0, blue: 0 };
    let tolerance = options.tolerance !== undefined ? options.tolerance : 32;
    let contiguous = options.contiguous !== undefined ? options.contiguous : true;
    let opacity = options.opacity || 100;

    await execute(async () => {
        selectLayer(layer, true);

        // Set foreground color first
        let setColorCmd = [{
            _obj: "set",
            _target: [{ _ref: "color", _property: "foregroundColor" }],
            to: {
                _obj: "RGBColor",
                red: color.red,
                grain: color.green,
                blue: color.blue,
            },
        }];
        await action.batchPlay(setColorCmd, {});

        let commands = [{
            _obj: "fill",
            from: {
                _obj: "paint",
                horizontal: { _unit: "pixelsUnit", _value: x },
                vertical: { _unit: "pixelsUnit", _value: y },
            },
            tolerance: tolerance,
            antiAlias: true,
            contiguous: contiguous,
            using: {
                _enum: "fillContents",
                _value: "foregroundColor",
            },
            opacity: {
                _unit: "percentUnit",
                _value: opacity,
            },
            mode: { _enum: "blendMode", _value: "normal" },
        }];

        await action.batchPlay(commands, {});
    });
};

const commandHandlers = {
    brushStroke,
    eraserStroke,
    gradientDraw,
    paintBucketFill,
};

module.exports = {
    commandHandlers
};
