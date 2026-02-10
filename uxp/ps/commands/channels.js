/* MIT License - Copyright (c) 2025 Mike Chambers / 00bx expansion */

const { app, action } = require("photoshop");

const {
    findLayer,
    execute,
    selectLayer,
    hasActiveSelection
} = require("./utils");

const selectAll = async (command) => {
    await execute(async () => {
        let commands = [{
            _obj: "set",
            _target: [{ _ref: "channel", _property: "selection" }],
            to: { _enum: "ordinal", _value: "allEnum" },
        }];
        await action.batchPlay(commands, {});
    });
};

const selectColorRange = async (command) => {
    let options = command.options;
    let color = options.color || { red: 255, green: 0, blue: 0 };
    let fuzziness = options.fuzziness !== undefined ? options.fuzziness : 40;

    await execute(async () => {
        let commands = [{
            _obj: "colorRange",
            fuzziness: fuzziness,
            minimum: {
                _obj: "RGBColor",
                red: color.red,
                grain: color.green,
                blue: color.blue,
            },
            maximum: {
                _obj: "RGBColor",
                red: color.red,
                grain: color.green,
                blue: color.blue,
            },
        }];

        await action.batchPlay(commands, {});
    });
};

const selectFocusArea = async (command) => {
    let options = command.options;
    let fuzziness = options.fuzziness !== undefined ? options.fuzziness : 0;

    await execute(async () => {
        let commands = [{
            _obj: "focusArea",
            focusAreaParam: fuzziness,
        }];

        await action.batchPlay(commands, {});
    });
};

const growSelection = async (command) => {
    if (!hasActiveSelection()) {
        throw new Error("growSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "grow",
        }];
        await action.batchPlay(commands, {});
    });
};

const similarSelection = async (command) => {
    if (!hasActiveSelection()) {
        throw new Error("similarSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "similar",
        }];
        await action.batchPlay(commands, {});
    });
};

const expandSelection = async (command) => {
    let options = command.options;
    let pixels = options.pixels || 1;

    if (!hasActiveSelection()) {
        throw new Error("expandSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "expand",
            by: {
                _unit: "pixelsUnit",
                _value: pixels,
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const contractSelection = async (command) => {
    let options = command.options;
    let pixels = options.pixels || 1;

    if (!hasActiveSelection()) {
        throw new Error("contractSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "contract",
            by: {
                _unit: "pixelsUnit",
                _value: pixels,
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const featherSelection = async (command) => {
    let options = command.options;
    let pixels = options.pixels || 5;

    if (!hasActiveSelection()) {
        throw new Error("featherSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "feather",
            radius: {
                _unit: "pixelsUnit",
                _value: pixels,
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const smoothSelection = async (command) => {
    let options = command.options;
    let sampleRadius = options.sampleRadius || 2;

    if (!hasActiveSelection()) {
        throw new Error("smoothSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "smoothness",
            radius: {
                _unit: "pixelsUnit",
                _value: sampleRadius,
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const borderSelection = async (command) => {
    let options = command.options;
    let width = options.width || 5;

    if (!hasActiveSelection()) {
        throw new Error("borderSelection : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "border",
            width: {
                _unit: "pixelsUnit",
                _value: width,
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const saveSelectionAsChannel = async (command) => {
    let options = command.options;
    let channelName = options.channelName || "Alpha 1";

    if (!hasActiveSelection()) {
        throw new Error("saveSelectionAsChannel : Requires an active selection");
    }

    await execute(async () => {
        let commands = [{
            _obj: "duplicate",
            _target: [{ _ref: "channel", _property: "selection" }],
            name: channelName,
        }];
        await action.batchPlay(commands, {});
    });
};

const loadSelectionFromChannel = async (command) => {
    let options = command.options;
    let channelName = options.channelName || "Alpha 1";

    await execute(async () => {
        let commands = [{
            _obj: "set",
            _target: [{ _ref: "channel", _property: "selection" }],
            to: {
                _ref: "channel",
                _name: channelName,
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const deleteChannel = async (command) => {
    let options = command.options;
    let channelName = options.channelName;

    if (!channelName) {
        throw new Error("deleteChannel : channelName is required");
    }

    await execute(async () => {
        let commands = [{
            _obj: "delete",
            _target: [{
                _ref: "channel",
                _name: channelName,
            }],
        }];
        await action.batchPlay(commands, {});
    });
};

const transformSelection = async (command) => {
    let options = command.options;

    if (!hasActiveSelection()) {
        throw new Error("transformSelection : Requires an active selection");
    }

    let width = options.width !== undefined ? options.width : 100;
    let height = options.height !== undefined ? options.height : 100;
    let angle = options.angle !== undefined ? options.angle : 0;

    await execute(async () => {
        let commands = [{
            _obj: "transform",
            _target: [{ _ref: "channel", _property: "selection" }],
            freeTransformCenterState: {
                _enum: "quadCenterState",
                _value: "QCSAverage",
            },
            width: { _unit: "percentUnit", _value: width },
            height: { _unit: "percentUnit", _value: height },
            angle: { _unit: "angleUnit", _value: angle },
            interfaceIconFrameDimmed: {
                _enum: "interpolationType",
                _value: "bicubicAutomatic",
            },
        }];
        await action.batchPlay(commands, {});
    });
};

const commandHandlers = {
    selectAll,
    selectColorRange,
    selectFocusArea,
    growSelection,
    similarSelection,
    expandSelection,
    contractSelection,
    featherSelection,
    smoothSelection,
    borderSelection,
    saveSelectionAsChannel,
    loadSelectionFromChannel,
    deleteChannel,
    transformSelection,
};

module.exports = {
    commandHandlers
};
