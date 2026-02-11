/* MIT License - Copyright (c) 2025 Mike Chambers / 00bx expansion */

const { app, action } = require("photoshop");

const { findLayer, execute, selectLayer } = require("./utils");

const drawRectangleShape = async (command) => {
  let options = command.options;
  let bounds = options.bounds || { top: 0, left: 0, bottom: 100, right: 100 };
  let fillColor = options.fillColor || { red: 255, green: 255, blue: 255 };
  let strokeColor = options.strokeColor || null;
  let strokeWidth = options.strokeWidth || 0;
  let cornerRadius = options.cornerRadius || 0;

  await execute(async () => {
    let shapeDesc = {
      _obj: "contentLayer",
      type: {
        _obj: "solidColorLayer",
        color: {
          _obj: "RGBColor",
          red: fillColor.red,
          grain: fillColor.green,
          blue: fillColor.blue,
        },
      },
      shape: {
        _obj: "rectangle",
        unitValueQuadVersion: 1,
        top: { _unit: "pixelsUnit", _value: bounds.top },
        left: { _unit: "pixelsUnit", _value: bounds.left },
        bottom: { _unit: "pixelsUnit", _value: bounds.bottom },
        right: { _unit: "pixelsUnit", _value: bounds.right },
        topLeft: { _unit: "pixelsUnit", _value: cornerRadius },
        topRight: { _unit: "pixelsUnit", _value: cornerRadius },
        bottomLeft: { _unit: "pixelsUnit", _value: cornerRadius },
        bottomRight: { _unit: "pixelsUnit", _value: cornerRadius },
      },
    };

    let strokeDesc = {};
    if (strokeColor && strokeWidth > 0) {
      strokeDesc = {
        strokeStyle: {
          _obj: "strokeStyle",
          strokeStyleVersion: 2,
          strokeEnabled: true,
          fillEnabled: true,
          strokeStyleLineWidth: {
            _unit: "pixelsUnit",
            _value: strokeWidth,
          },
          strokeStyleContent: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: strokeColor.red,
              grain: strokeColor.green,
              blue: strokeColor.blue,
            },
          },
        },
      };
    }

    let commands = [
      {
        _obj: "make",
        _target: [{ _ref: "contentLayer" }],
        using: { ...shapeDesc, ...strokeDesc },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const drawEllipseShape = async (command) => {
  let options = command.options;
  let bounds = options.bounds || { top: 0, left: 0, bottom: 100, right: 100 };
  let fillColor = options.fillColor || { red: 255, green: 255, blue: 255 };
  let strokeColor = options.strokeColor || null;
  let strokeWidth = options.strokeWidth || 0;

  await execute(async () => {
    let shapeDesc = {
      _obj: "contentLayer",
      type: {
        _obj: "solidColorLayer",
        color: {
          _obj: "RGBColor",
          red: fillColor.red,
          grain: fillColor.green,
          blue: fillColor.blue,
        },
      },
      shape: {
        _obj: "ellipse",
        unitValueQuadVersion: 1,
        top: { _unit: "pixelsUnit", _value: bounds.top },
        left: { _unit: "pixelsUnit", _value: bounds.left },
        bottom: { _unit: "pixelsUnit", _value: bounds.bottom },
        right: { _unit: "pixelsUnit", _value: bounds.right },
      },
    };

    let strokeDesc = {};
    if (strokeColor && strokeWidth > 0) {
      strokeDesc = {
        strokeStyle: {
          _obj: "strokeStyle",
          strokeStyleVersion: 2,
          strokeEnabled: true,
          fillEnabled: true,
          strokeStyleLineWidth: {
            _unit: "pixelsUnit",
            _value: strokeWidth,
          },
          strokeStyleContent: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: strokeColor.red,
              grain: strokeColor.green,
              blue: strokeColor.blue,
            },
          },
        },
      };
    }

    let commands = [
      {
        _obj: "make",
        _target: [{ _ref: "contentLayer" }],
        using: { ...shapeDesc, ...strokeDesc },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const drawLineShape = async (command) => {
  let options = command.options;
  let startPoint = options.startPoint || { x: 0, y: 0 };
  let endPoint = options.endPoint || { x: 100, y: 100 };
  let strokeColor = options.strokeColor || { red: 255, green: 255, blue: 255 };
  let strokeWidth = options.strokeWidth || 2;

  await execute(async () => {
    let commands = [
      {
        _obj: "make",
        _target: [{ _ref: "contentLayer" }],
        using: {
          _obj: "contentLayer",
          type: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: strokeColor.red,
              grain: strokeColor.green,
              blue: strokeColor.blue,
            },
          },
          shape: {
            _obj: "pathClass",
            pathComponents: [
              {
                _obj: "pathComponent",
                shapeOperation: { _enum: "shapeOperation", _value: "add" },
                subpathListKey: [
                  {
                    _obj: "subpathsList",
                    closedSubpath: false,
                    points: [
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: {
                            _unit: "pixelsUnit",
                            _value: startPoint.x,
                          },
                          vertical: {
                            _unit: "pixelsUnit",
                            _value: startPoint.y,
                          },
                        },
                      },
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: {
                            _unit: "pixelsUnit",
                            _value: endPoint.x,
                          },
                          vertical: { _unit: "pixelsUnit", _value: endPoint.y },
                        },
                      },
                    ],
                  },
                ],
              },
            ],
          },
          strokeStyle: {
            _obj: "strokeStyle",
            strokeStyleVersion: 2,
            strokeEnabled: true,
            fillEnabled: false,
            strokeStyleLineWidth: { _unit: "pixelsUnit", _value: strokeWidth },
            strokeStyleLineCap: {
              _enum: "strokeStyleLineCap",
              _value: "strokeStyleRoundCap",
            },
            strokeStyleContent: {
              _obj: "solidColorLayer",
              color: {
                _obj: "RGBColor",
                red: strokeColor.red,
                grain: strokeColor.green,
                blue: strokeColor.blue,
              },
            },
          },
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const drawPolygonShape = async (command) => {
  let options = command.options;
  let sides = options.sides || 6;
  let centerX = options.centerX || 100;
  let centerY = options.centerY || 100;
  let radius = options.radius || 50;
  let fillColor = options.fillColor || { red: 255, green: 255, blue: 255 };
  let strokeColor = options.strokeColor || null;
  let strokeWidth = options.strokeWidth || 0;

  // Build polygon points manually
  let points = [];
  for (let i = 0; i < sides; i++) {
    let angle = (2 * Math.PI * i) / sides - Math.PI / 2;
    points.push({
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    });
  }

  await execute(async () => {
    let pathPoints = points.map((p) => ({
      _obj: "pathPoint",
      anchor: {
        _obj: "paint",
        horizontal: { _unit: "pixelsUnit", _value: p.x },
        vertical: { _unit: "pixelsUnit", _value: p.y },
      },
    }));

    let strokeDesc = {};
    if (strokeColor && strokeWidth > 0) {
      strokeDesc = {
        strokeStyle: {
          _obj: "strokeStyle",
          strokeStyleVersion: 2,
          strokeEnabled: true,
          fillEnabled: true,
          strokeStyleLineWidth: {
            _unit: "pixelsUnit",
            _value: strokeWidth,
          },
          strokeStyleContent: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: strokeColor.red,
              grain: strokeColor.green,
              blue: strokeColor.blue,
            },
          },
        },
      };
    }

    let commands = [
      {
        _obj: "make",
        _target: [{ _ref: "contentLayer" }],
        using: {
          _obj: "contentLayer",
          type: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: fillColor.red,
              grain: fillColor.green,
              blue: fillColor.blue,
            },
          },
          shape: {
            _obj: "pathClass",
            pathComponents: [
              {
                _obj: "pathComponent",
                shapeOperation: {
                  _enum: "shapeOperation",
                  _value: "add",
                },
                subpathListKey: [
                  {
                    _obj: "subpathsList",
                    closedSubpath: true,
                    points: pathPoints,
                  },
                ],
              },
            ],
          },
          ...strokeDesc,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const drawCustomPath = async (command) => {
  let options = command.options;
  let points = options.points || [];
  let closed = options.closed !== undefined ? options.closed : true;
  let fillColor = options.fillColor || { red: 255, green: 255, blue: 255 };
  let strokeColor = options.strokeColor || null;
  let strokeWidth = options.strokeWidth || 0;

  if (points.length < 2) {
    throw new Error("drawCustomPath : At least 2 points are required");
  }

  await execute(async () => {
    let pathPoints = points.map((p) => {
      // Support both formats: {leftDirection: {x,y}} and {handleInX, handleInY}
      let leftDir = p.leftDirection;
      if (!leftDir && p.handleInX !== undefined && p.handleInY !== undefined) {
        leftDir = { x: p.handleInX, y: p.handleInY };
      }
      let rightDir = p.rightDirection;
      if (
        !rightDir &&
        p.handleOutX !== undefined &&
        p.handleOutY !== undefined
      ) {
        rightDir = { x: p.handleOutX, y: p.handleOutY };
      }

      let desc = {
        _obj: "pathPoint",
        anchor: {
          _obj: "paint",
          horizontal: { _unit: "pixelsUnit", _value: p.x },
          vertical: { _unit: "pixelsUnit", _value: p.y },
        },
      };

      if (leftDir) {
        desc.leftDirection = {
          _obj: "paint",
          horizontal: { _unit: "pixelsUnit", _value: leftDir.x },
          vertical: { _unit: "pixelsUnit", _value: leftDir.y },
        };
      }

      if (rightDir) {
        desc.rightDirection = {
          _obj: "paint",
          horizontal: { _unit: "pixelsUnit", _value: rightDir.x },
          vertical: { _unit: "pixelsUnit", _value: rightDir.y },
        };
      }

      return desc;
    });

    let strokeDesc = {};
    if (strokeColor && strokeWidth > 0) {
      strokeDesc = {
        strokeStyle: {
          _obj: "strokeStyle",
          strokeStyleVersion: 2,
          strokeEnabled: true,
          fillEnabled: true,
          strokeStyleLineWidth: {
            _unit: "pixelsUnit",
            _value: strokeWidth,
          },
          strokeStyleContent: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: strokeColor.red,
              grain: strokeColor.green,
              blue: strokeColor.blue,
            },
          },
        },
      };
    }

    let commands = [
      {
        _obj: "make",
        _target: [{ _ref: "contentLayer" }],
        using: {
          _obj: "contentLayer",
          type: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: fillColor.red,
              grain: fillColor.green,
              blue: fillColor.blue,
            },
          },
          shape: {
            _obj: "pathClass",
            pathComponents: [
              {
                _obj: "pathComponent",
                shapeOperation: {
                  _enum: "shapeOperation",
                  _value: "add",
                },
                subpathListKey: [
                  {
                    _obj: "subpathsList",
                    closedSubpath: closed,
                    points: pathPoints,
                  },
                ],
              },
            ],
          },
          ...strokeDesc,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const drawArrowShape = async (command) => {
  let options = command.options;
  let startPoint = options.startPoint || { x: 0, y: 0 };
  let endPoint = options.endPoint || { x: 100, y: 100 };
  let strokeColor = options.strokeColor || { red: 255, green: 255, blue: 255 };
  let strokeWidth = options.strokeWidth || 2;
  let headSize = options.headSize || 12;

  await execute(async () => {
    // Calculate arrow direction
    let dx = endPoint.x - startPoint.x;
    let dy = endPoint.y - startPoint.y;
    let len = Math.sqrt(dx * dx + dy * dy);
    if (len === 0) len = 1;
    let ux = dx / len;
    let uy = dy / len;

    // Arrowhead base point (where head meets shaft)
    let baseX = endPoint.x - ux * headSize;
    let baseY = endPoint.y - uy * headSize;

    // Perpendicular for arrowhead wings
    let px = -uy * headSize * 0.5;
    let py = ux * headSize * 0.5;

    let wingL = { x: baseX + px, y: baseY + py };
    let wingR = { x: baseX - px, y: baseY - py };

    // Draw shaft as open path
    let shaftCommands = [
      {
        _obj: "make",
        _target: [{ _ref: "contentLayer" }],
        using: {
          _obj: "contentLayer",
          type: {
            _obj: "solidColorLayer",
            color: {
              _obj: "RGBColor",
              red: strokeColor.red,
              grain: strokeColor.green,
              blue: strokeColor.blue,
            },
          },
          shape: {
            _obj: "pathClass",
            pathComponents: [
              {
                _obj: "pathComponent",
                shapeOperation: { _enum: "shapeOperation", _value: "add" },
                subpathListKey: [
                  {
                    _obj: "subpathsList",
                    closedSubpath: false,
                    points: [
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: {
                            _unit: "pixelsUnit",
                            _value: startPoint.x,
                          },
                          vertical: {
                            _unit: "pixelsUnit",
                            _value: startPoint.y,
                          },
                        },
                      },
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: { _unit: "pixelsUnit", _value: baseX },
                          vertical: { _unit: "pixelsUnit", _value: baseY },
                        },
                      },
                    ],
                  },
                  {
                    _obj: "subpathsList",
                    closedSubpath: true,
                    points: [
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: {
                            _unit: "pixelsUnit",
                            _value: endPoint.x,
                          },
                          vertical: { _unit: "pixelsUnit", _value: endPoint.y },
                        },
                      },
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: { _unit: "pixelsUnit", _value: wingL.x },
                          vertical: { _unit: "pixelsUnit", _value: wingL.y },
                        },
                      },
                      {
                        _obj: "pathPoint",
                        anchor: {
                          _obj: "paint",
                          horizontal: { _unit: "pixelsUnit", _value: wingR.x },
                          vertical: { _unit: "pixelsUnit", _value: wingR.y },
                        },
                      },
                    ],
                  },
                ],
              },
            ],
          },
          strokeStyle: {
            _obj: "strokeStyle",
            strokeStyleVersion: 2,
            strokeEnabled: true,
            fillEnabled: true,
            strokeStyleLineWidth: { _unit: "pixelsUnit", _value: strokeWidth },
            strokeStyleLineCap: {
              _enum: "strokeStyleLineCap",
              _value: "strokeStyleRoundCap",
            },
            strokeStyleContent: {
              _obj: "solidColorLayer",
              color: {
                _obj: "RGBColor",
                red: strokeColor.red,
                grain: strokeColor.green,
                blue: strokeColor.blue,
              },
            },
          },
        },
      },
    ];

    await action.batchPlay(shaftCommands, {});
  });
};

const commandHandlers = {
  drawRectangleShape,
  drawEllipseShape,
  drawLineShape,
  drawPolygonShape,
  drawCustomPath,
  drawArrowShape,
};

module.exports = {
  commandHandlers,
};
