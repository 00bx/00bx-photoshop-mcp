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

const { app, constants, action, imaging } = require("photoshop");
const fs = require("uxp").storage.localFileSystem;

const {
  _saveDocumentAs,
  parseColor,
  getAlignmentMode,
  getNewDocumentMode,
  selectLayer,
  findLayer,
  findLayerByName,
  execute,
  tokenify,
  hasActiveSelection,
  listOpenDocuments,
} = require("./utils");

const { rasterizeLayer } = require("./layers").commandHandlers;

const openFile = async (command) => {
  let options = command.options;

  await execute(async () => {
    let entry = null;
    try {
      entry = await fs.getEntryWithUrl("file:" + options.filePath);
    } catch (e) {
      throw new Error(
        "openFile: Could not create file entry. File probably does not exist.",
      );
    }

    await app.open(entry);
  });
};

const placeImage = async (command) => {
  let options = command.options;
  let layerId = options.layerId;
  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`placeImage : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);
    let layerId = layer.id;

    let imagePath = await tokenify(options.imagePath);

    let commands = [
      // Place
      {
        ID: layerId,
        _obj: "placeEvent",
        freeTransformCenterState: {
          _enum: "quadCenterState",
          _value: "QCSAverage",
        },
        null: {
          _kind: "local",
          _path: imagePath,
        },
        offset: {
          _obj: "offset",
          horizontal: {
            _unit: "pixelsUnit",
            _value: 0.0,
          },
          vertical: {
            _unit: "pixelsUnit",
            _value: 0.0,
          },
        },
        replaceLayer: {
          _obj: "placeEvent",
          to: {
            _id: layerId,
            _ref: "layer",
          },
        },
      },
      {
        _obj: "set",
        _target: [
          {
            _enum: "ordinal",
            _ref: "layer",
            _value: "targetEnum",
          },
        ],
        to: {
          _obj: "layer",
          name: layerId,
        },
      },
    ];

    await action.batchPlay(commands, {});
    await rasterizeLayer(command);
  });
};

const getDocumentImage = async (command) => {
  let out = await execute(async () => {
    const pixelsOpt = {
      applyAlpha: true,
    };

    const imgObj = await imaging.getPixels(pixelsOpt);

    const base64Data = await imaging.encodeImageData({
      imageData: imgObj.imageData,
      base64: true,
    });

    const result = {
      base64Image: base64Data,
      dataUrl: `data:image/jpeg;base64,${base64Data}`,
      width: imgObj.imageData.width,
      height: imgObj.imageData.height,
      colorSpace: imgObj.imageData.colorSpace,
      components: imgObj.imageData.components,
      format: "jpeg",
    };

    imgObj.imageData.dispose();
    return result;
  });

  return out;
};

const getDocumentInfo = async (command) => {
  let doc = app.activeDocument;
  let path = doc.path;

  let out = {
    height: doc.height,
    width: doc.width,
    colorMode: doc.mode.toString(),
    pixelAspectRatio: doc.pixelAspectRatio,
    resolution: doc.resolution,
    path: path,
    saved: path.length > 0,
    hasUnsavedChanges: !doc.saved,
  };

  return out;
};

const cropDocument = async (command) => {
  let options = command.options;

  if (!hasActiveSelection()) {
    throw new Error("cropDocument : Requires an active selection");
  }

  return await execute(async () => {
    let commands = [
      // Crop
      {
        _obj: "crop",
        delete: true,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const removeBackground = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`removeBackground : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      // Remove Background
      {
        _obj: "removeBackground",
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const alignContent = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`alignContent : Could not find layerId : ${layerId}`);
  }

  if (!app.activeDocument.selection.bounds) {
    throw new Error(`alignContent : Requires an active selection`);
  }

  await execute(async () => {
    let m = getAlignmentMode(options.alignmentMode);

    selectLayer(layer, true);

    let commands = [
      {
        _obj: "align",
        _target: [
          {
            _enum: "ordinal",
            _ref: "layer",
            _value: "targetEnum",
          },
        ],
        alignToCanvas: false,
        using: {
          _enum: "alignDistributeSelector",
          _value: m,
        },
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const generateImage = async (command) => {
  let options = command.options;

  await execute(async () => {
    let doc = app.activeDocument;

    await doc.selection.selectAll();

    let contentType = "none";
    if (options.contentType) {
      const c = options.contentType.toLowerCase();
      if (c === "photo" || c === "art") {
        contentType = c;
      }
    }

    let commands = [
      // Generate Image current document
      {
        _obj: "syntheticTextToImage",
        _target: [
          {
            _enum: "ordinal",
            _ref: "document",
            _value: "targetEnum",
          },
        ],
        documentID: doc.id,
        layerID: 0,
        prompt: options.prompt,
        serviceID: "clio",
        serviceOptionsList: {
          clio: {
            _obj: "clio",
            clio_advanced_options: {
              text_to_image_styles_options: {
                text_to_image_content_type: contentType,
                text_to_image_effects_count: 0,
                text_to_image_effects_list: ["none", "none", "none"],
              },
            },
            dualCrop: true,
            gentech_workflow_name: "text_to_image",
            gi_ADVANCED: '{"enable_mts":true}',
            gi_CONTENT_PRESERVE: 0,
            gi_CROP: false,
            gi_DILATE: false,
            gi_ENABLE_PROMPT_FILTER: true,
            gi_GUIDANCE: 6,
            gi_MODE: "ginp",
            gi_NUM_STEPS: -1,
            gi_PROMPT: options.prompt,
            gi_SEED: -1,
            gi_SIMILARITY: 0,
          },
        },
        workflow: "text_to_image",
        workflowType: {
          _enum: "genWorkflow",
          _value: "text_to_image",
        },
      },
      // Rasterize current layer
      {
        _obj: "rasterizeLayer",
        _target: [
          {
            _enum: "ordinal",
            _ref: "layer",
            _value: "targetEnum",
          },
        ],
      },
    ];
    let o = await action.batchPlay(commands, {});

    // Firefly may return layerID in the result, or we fall back to the active layer
    let genLayerId = o && o[0] ? o[0].layerID : undefined;
    let l = genLayerId ? findLayer(genLayerId) : null;

    // Fallback: grab the currently active (topmost selected) layer
    if (!l) {
      let allLayers = app.activeDocument.layers;
      for (const candidate of allLayers) {
        if (candidate.selected) {
          l = candidate;
          break;
        }
      }
    }

    // Last resort: just use the top layer (Firefly always creates on top)
    if (!l && app.activeDocument.layers.length > 0) {
      l = app.activeDocument.layers[0];
    }

    if (l) {
      l.name = options.layerName;
    }
  });
};

const generativeFill = async (command) => {
  const options = command.options;
  const layerId = options.layerId;
  const prompt = options.prompt;

  const layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`generativeFill : Could not find layerId : ${layerId}`);
  }

  if (!hasActiveSelection()) {
    throw new Error(`generativeFill : Requires an active selection.`);
  }

  await execute(async () => {
    let doc = app.activeDocument;

    let contentType = "none";
    if (options.contentType) {
      const c = options.contentType.toLowerCase();
      if (c === "photo" || c === "art") {
        contentType = c;
      }
    }

    let commands = [
      // Generative Fill current document
      {
        _obj: "syntheticFill",
        _target: [
          {
            _enum: "ordinal",
            _ref: "document",
            _value: "targetEnum",
          },
        ],
        documentID: doc.id,
        layerID: layerId,
        prompt: prompt,
        serviceID: "clio",
        serviceOptionsList: {
          clio: {
            _obj: "clio",
            dualCrop: true,
            gi_ADVANCED: '{"enable_mts":true}',
            gi_CONTENT_PRESERVE: 0,
            gi_CROP: false,
            gi_DILATE: false,
            gi_ENABLE_PROMPT_FILTER: true,
            gi_GUIDANCE: 6,
            gi_MODE: "tinp",
            gi_NUM_STEPS: -1,
            gi_PROMPT: prompt,
            gi_SEED: -1,
            gi_SIMILARITY: 0,

            clio_advanced_options: {
              text_to_image_styles_options: {
                text_to_image_content_type: contentType,
                text_to_image_effects_count: 0,
                text_to_image_effects_list: ["none", "none", "none"],
              },
            },
          },
        },
        serviceVersion: "clio3",
        workflowType: {
          _enum: "genWorkflow",
          _value: "in_painting",
        },
        workflow_to_active_service_identifier_map: {
          gen_harmonize: "clio3",
          generate_background: "clio3",
          generate_similar: "clio3",
          generativeUpscale: "fal_aura_sr",
          in_painting: "clio3",
          instruct_edit: "clio3",
          out_painting: "clio3",
          text_to_image: "clio3",
        },
      },
    ];

    let o = await action.batchPlay(commands, {});

    // Firefly may return layerID in the result, or we fall back
    let genLayerId = o && o[0] ? o[0].layerID : undefined;
    let l = genLayerId ? findLayer(genLayerId) : null;

    // Fallback: grab the currently active (topmost selected) layer
    if (!l) {
      let allLayers = app.activeDocument.layers;
      for (const candidate of allLayers) {
        if (candidate.selected) {
          l = candidate;
          break;
        }
      }
    }

    // Last resort: top layer (Firefly creates on top)
    if (!l && app.activeDocument.layers.length > 0) {
      l = app.activeDocument.layers[0];
    }

    if (l) {
      l.name = options.layerName;
    }
  });
};

const saveDocument = async (command) => {
  await execute(async () => {
    await app.activeDocument.save();
  });
};

const saveDocumentAs = async (command) => {
  let options = command.options;

  return await _saveDocumentAs(options.filePath, options.fileType);
};

const setActiveDocument = async (command) => {
  let options = command.options;
  let documentId = options.documentId;
  let docs = listOpenDocuments();

  for (let doc of docs) {
    if (doc.id === documentId) {
      await execute(async () => {
        app.activeDocument = doc;
      });

      return;
    }
  }
};

const getDocuments = async (command) => {
  return listOpenDocuments();
};

const duplicateDocument = async (command) => {
  let options = command.options;
  let name = options.name;

  await execute(async () => {
    const doc = app.activeDocument;
    await doc.duplicate(name);
  });
};

const createDocument = async (command) => {
  let options = command.options;
  let colorMode = getNewDocumentMode(command.options.colorMode);
  let fillColor = parseColor(options.fillColor);

  await execute(async () => {
    await app.createDocument({
      typename: "DocumentCreateOptions",
      width: options.width,
      height: options.height,
      resolution: options.resolution,
      mode: colorMode,
      fill: constants.DocumentFill.COLOR,
      fillColor: fillColor,
      profile: "sRGB IEC61966-2.1",
    });

    let background = findLayerByName("Background");
    background.allLocked = false;
    background.name = "Background";
  });
};

const executeBatchPlayCommand = async (commands) => {
  console.log("BATCHPLAY_V2_LOADED — executeBatchPlayCommand invoked");
  let options = commands.options;
  let c = options.commands;
  let layerId = options.layerId || null;

  let out = await execute(async () => {
    // If a layerId was provided, select that layer first (same pattern as all working tools)
    if (layerId) {
      let layer = findLayer(layerId);
      if (!layer) {
        throw new Error(
          `executeBatchPlayCommand: Could not find layerId: ${layerId}`,
        );
      }
      selectLayer(layer, true);
      console.log(
        `executeBatchPlayCommand: Selected layer ${layerId} (${layer.name})`,
      );
    }

    try {
      let results = await action.batchPlay(c, {});
      console.log("executeBatchPlayCommand results:", JSON.stringify(results));
      return results;
    } catch (err) {
      console.error("executeBatchPlayCommand batchPlay error:", err);
      throw err;
    }
  });

  return out;
};

const resizeImage = async (command) => {
  let options = command.options;
  let width = options.width;
  let height = options.height;
  let resolution = options.resolution || undefined;
  let interpolation = options.interpolation || "bicubicAutomatic";

  await execute(async () => {
    let desc = {
      _obj: "imageSize",
      constrainProportions: options.constrain !== false,
      interfaceIconFrameDimmed: {
        _enum: "interpolationType",
        _value: interpolation,
      },
    };

    if (width) desc.width = { _unit: "pixelsUnit", _value: width };
    if (height) desc.height = { _unit: "pixelsUnit", _value: height };
    if (resolution)
      desc.resolution = { _unit: "densityUnit", _value: resolution };

    await action.batchPlay([desc], {});
  });
};

const resizeCanvas = async (command) => {
  let options = command.options;
  let width = options.width;
  let height = options.height;
  let anchor = options.anchor || "MIDDLECENTER";
  let color = options.color || null;

  await execute(async () => {
    let desc = {
      _obj: "canvasSize",
      width: { _unit: "pixelsUnit", _value: width },
      height: { _unit: "pixelsUnit", _value: height },
      horizontal: {
        _enum: "horizontalLocation",
        _value: anchor.includes("LEFT")
          ? "left"
          : anchor.includes("RIGHT")
            ? "right"
            : "center",
      },
      vertical: {
        _enum: "verticalLocation",
        _value: anchor.includes("TOP")
          ? "top"
          : anchor.includes("BOTTOM")
            ? "bottom"
            : "center",
      },
    };

    if (color) {
      desc.canvasExtensionColorType = {
        _enum: "canvasExtensionColorType",
        _value: "color",
      };
      desc.canvasExtensionColor = {
        _obj: "RGBColor",
        red: color.red,
        grain: color.green,
        blue: color.blue,
      };
    }

    await action.batchPlay([desc], {});
  });
};

const rotateCanvas = async (command) => {
  let options = command.options;
  let angle = options.angle || 90;

  await execute(async () => {
    let commands = [
      {
        _obj: "rotateEventEnum",
        angle: {
          _unit: "angleUnit",
          _value: angle,
        },
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const trimDocument = async (command) => {
  let options = command.options;
  let trimType = options.trimType || "transparent";

  let typeMap = {
    transparent: "transparency",
    topLeft: "topLeftPixelColor",
    bottomRight: "bottomRightPixelColor",
  };

  let top = options.top !== false;
  let left = options.left !== false;
  let bottom = options.bottom !== false;
  let right = options.right !== false;

  await execute(async () => {
    let commands = [
      {
        _obj: "trim",
        trimBasedOn: {
          _enum: "trimBasedOn",
          _value: typeMap[trimType] || "transparency",
        },
        top: top,
        left: left,
        bottom: bottom,
        right: right,
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const revealAll = async (command) => {
  await execute(async () => {
    let commands = [
      {
        _obj: "revealAll",
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const mergeVisible = async (command) => {
  await execute(async () => {
    let commands = [
      {
        _obj: "mergeVisible",
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const mergeDown = async (command) => {
  let options = command.options;
  let layerId = options.layerId;
  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`mergeDown : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);
    let commands = [
      {
        _obj: "mergeLayersNew",
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const stampVisible = async (command) => {
  await execute(async () => {
    let commands = [
      {
        _obj: "mergeVisible",
        duplicate: true,
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const setForegroundColor = async (command) => {
  let options = command.options;
  let color = options.color || { red: 0, green: 0, blue: 0 };

  await execute(async () => {
    let commands = [
      {
        _obj: "set",
        _target: [{ _ref: "color", _property: "foregroundColor" }],
        to: {
          _obj: "RGBColor",
          red: color.red,
          grain: color.green,
          blue: color.blue,
        },
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const setBackgroundColor = async (command) => {
  let options = command.options;
  let color = options.color || { red: 255, green: 255, blue: 255 };

  await execute(async () => {
    let commands = [
      {
        _obj: "set",
        _target: [{ _ref: "color", _property: "backgroundColor" }],
        to: {
          _obj: "RGBColor",
          red: color.red,
          grain: color.green,
          blue: color.blue,
        },
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const swapColors = async (command) => {
  await execute(async () => {
    let commands = [
      {
        _obj: "exchange",
        _target: [{ _ref: "color", _property: "colors" }],
      },
    ];
    await action.batchPlay(commands, {});
  });
};

const commandHandlers = {
  generativeFill,
  executeBatchPlayCommand,
  setActiveDocument,
  getDocuments,
  duplicateDocument,
  getDocumentImage,
  openFile,
  placeImage,
  getDocumentInfo,
  cropDocument,
  removeBackground,
  alignContent,
  generateImage,
  saveDocument,
  saveDocumentAs,
  createDocument,
  resizeImage,
  resizeCanvas,
  rotateCanvas,
  trimDocument,
  revealAll,
  mergeVisible,
  mergeDown,
  stampVisible,
  setForegroundColor,
  setBackgroundColor,
  swapColors,
};

module.exports = {
  commandHandlers,
};
