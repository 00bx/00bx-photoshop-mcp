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

const { app, action, constants } = require("photoshop");

const { findLayer, execute, selectLayer } = require("./utils");

// --- Existing filters ---

const applyMotionBlur = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyMotionBlur : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    await layer.applyMotionBlur(options.angle, options.distance);
  });
};

const applyGaussianBlur = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyGaussianBlur : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    await layer.applyGaussianBlur(options.radius);
  });
};

const applyNoise = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyNoise : Could not find layerId : ${layerId}`);
  }

  const amount = options.amount || 5;
  const distStr = (options.distribution || "gaussian").toUpperCase();
  const distribution =
    constants.NoiseDistribution[distStr] ||
    constants.NoiseDistribution.GAUSSIAN;
  const monochromatic = options.monochromatic !== false;

  await execute(async () => {
    await layer.applyAddNoise(amount, distribution, monochromatic);
  });
};

// --- New filters ---

const applySharpen = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applySharpen : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "sharpen",
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyUnsharpMask = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyUnsharpMask : Could not find layerId : ${layerId}`);
  }

  const amount = options.amount || 100;
  const radius = options.radius || 1.0;
  const threshold = options.threshold || 0;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "unsharpMask",
        amount: amount,
        radius: {
          _unit: "pixelsUnit",
          _value: radius,
        },
        threshold: threshold,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyHighPass = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyHighPass : Could not find layerId : ${layerId}`);
  }

  const radius = options.radius || 10.0;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "highPass",
        radius: {
          _unit: "pixelsUnit",
          _value: radius,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyRadialBlur = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyRadialBlur : Could not find layerId : ${layerId}`);
  }

  const amount = options.amount || 10;
  const method = options.method || "spin";
  const quality = options.quality || "good";

  const methodMap = {
    spin: "spin",
    zoom: "zoom",
  };

  const qualityMap = {
    draft: "draft",
    good: "good",
    best: "best",
  };

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "radialBlur",
        amount: amount,
        blurMethod: {
          _enum: "blurMethod",
          _value: methodMap[method] || "spin",
        },
        blurQuality: {
          _enum: "blurQuality",
          _value: qualityMap[quality] || "good",
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applySurfaceBlur = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applySurfaceBlur : Could not find layerId : ${layerId}`);
  }

  const radius = options.radius || 5;
  const threshold = options.threshold || 15;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "surfaceBlur",
        radius: radius,
        threshold: threshold,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyLensBlur = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyLensBlur : Could not find layerId : ${layerId}`);
  }

  const radius = options.radius || 15;
  const brightness = options.brightness || 0;
  const threshold = options.threshold || 0;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "lensBlur",
        source: {
          _enum: "depthMapSource",
          _value: "none",
        },
        focalDistance: 0,
        radius: radius,
        brightness: brightness,
        threshold: threshold,
        noiseAmount: 0,
        distribution: {
          _enum: "distribution",
          _value: "uniform",
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applySmartSharpen = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applySmartSharpen : Could not find layerId : ${layerId}`);
  }

  const amount = options.amount || 100;
  const radius = options.radius || 1.0;
  const noiseReduction = options.noiseReduction || 0;
  const removeType = options.removeType || "gaussianBlur";

  const removeMap = {
    gaussianBlur: "gaussianBlur",
    lensBlur: "lensBlur",
    motionBlur: "motionBlur",
  };

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "smartSharpen",
        amount: amount,
        radius: {
          _unit: "pixelsUnit",
          _value: radius,
        },
        noiseReduction: noiseReduction,
        remove: {
          _enum: "removeType",
          _value: removeMap[removeType] || "gaussianBlur",
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyOilPaint = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyOilPaint : Could not find layerId : ${layerId}`);
  }

  const stylization = options.stylization || 4.0;
  const cleanliness = options.cleanliness || 5.0;
  const scale = options.scale || 0.5;
  const bristleDetail = options.bristleDetail || 2.0;
  const lighting = options.lighting !== false;
  const lightDirection = options.lightDirection || 0;
  const shine = options.shine || 0.5;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "GEfc",
        oilPaint: {
          _obj: "paintOil",
          lightingOn: lighting,
          stylization: stylization,
          cleanliness: cleanliness,
          brushScale: scale,
          bristleDetail: bristleDetail,
          angularDirection: lightDirection,
          shininess: shine,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyEmboss = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyEmboss : Could not find layerId : ${layerId}`);
  }

  const angle = options.angle || 135;
  const height = options.height || 3;
  const amount = options.amount || 100;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "emboss",
        angle: angle,
        height: height,
        amount: {
          _unit: "percentUnit",
          _value: amount,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyFindEdges = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyFindEdges : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "findEdges",
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyPixelate = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyPixelate : Could not find layerId : ${layerId}`);
  }

  const cellSize = options.cellSize || 10;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "mosaic",
        cellSize: {
          _unit: "pixelsUnit",
          _value: cellSize,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyCrystallize = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyCrystallize : Could not find layerId : ${layerId}`);
  }

  const cellSize = options.cellSize || 10;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "crystallize",
        cellSize: cellSize,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyColorHalftone = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyColorHalftone : Could not find layerId : ${layerId}`);
  }

  const maxRadius = options.maxRadius || 8;
  const angle1 = options.angle1 || 108;
  const angle2 = options.angle2 || 162;
  const angle3 = options.angle3 || 90;
  const angle4 = options.angle4 || 45;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "colorHalftone",
        maxRadius: maxRadius,
        angle1: angle1,
        angle2: angle2,
        angle3: angle3,
        angle4: angle4,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyTwirlDistortion = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(
      `applyTwirlDistortion : Could not find layerId : ${layerId}`,
    );
  }

  const angle = options.angle || 50;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "twirl",
        angle: angle,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyZigZagDistortion = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(
      `applyZigZagDistortion : Could not find layerId : ${layerId}`,
    );
  }

  const amount = options.amount || 10;
  const ridges = options.ridges || 5;
  const style = options.style || "pondRipples";

  const styleMap = {
    aroundCenter: "aroundCenter",
    outFromCenter: "outFromCenter",
    pondRipples: "pondRipples",
  };

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "zigZag",
        amount: amount,
        ridges: ridges,
        style: {
          _enum: "zigZagType",
          _value: styleMap[style] || "pondRipples",
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applySolarize = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applySolarize : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "solarize",
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyPosterize = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyPosterize : Could not find layerId : ${layerId}`);
  }

  const levels = options.levels || 4;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "posterize",
        levels: levels,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyDespeckle = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyDespeckle : Could not find layerId : ${layerId}`);
  }

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "despeckle",
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyMedianNoise = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(`applyMedianNoise : Could not find layerId : ${layerId}`);
  }

  const radius = options.radius || 1;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "median",
        radius: {
          _unit: "pixelsUnit",
          _value: radius,
        },
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const applyDustAndScratches = async (command) => {
  let options = command.options;
  let layerId = options.layerId;

  let layer = findLayer(layerId);

  if (!layer) {
    throw new Error(
      `applyDustAndScratches : Could not find layerId : ${layerId}`,
    );
  }

  const radius = options.radius || 1;
  const threshold = options.threshold || 0;

  await execute(async () => {
    selectLayer(layer, true);

    let commands = [
      {
        _obj: "dustAndScratches",
        radius: radius,
        threshold: threshold,
      },
    ];

    await action.batchPlay(commands, {});
  });
};

const commandHandlers = {
  applyMotionBlur,
  applyGaussianBlur,
  applyNoise,
  applySharpen,
  applyUnsharpMask,
  applyHighPass,
  applyRadialBlur,
  applySurfaceBlur,
  applyLensBlur,
  applySmartSharpen,
  applyOilPaint,
  applyEmboss,
  applyFindEdges,
  applyPixelate,
  applyCrystallize,
  applyColorHalftone,
  applyTwirlDistortion,
  applyZigZagDistortion,
  applySolarize,
  applyPosterize,
  applyDespeckle,
  applyMedianNoise,
  applyDustAndScratches,
};

module.exports = {
  commandHandlers,
};
