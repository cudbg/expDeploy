var fs = require('fs');
var seedrandom = require('seedrandom');
var d3 = require('d3');

var exponents = [1, 5, 10];
var max_positions = [0, 0.25, 1];
var heights = [0.22, 0.32, 0.47, 0.69, 0.85];
var fpss = [30];
var noises = [0];
var duration = 10;
var marking = "color";
var seed = "perceptvis";
var drop_type = "copy";
var drop_percents = [0, 0.1, 0.2, 0.3, 0.4];
var jsonData = [];
var datum;

// Transforms a dataset using between frame approximation
// @param frames: Dataset to transform
// @param drop_count: Number of frames to remove
// @param drop_type: How to fill in the dropped frame, either "copy" or "interpolate"
// @return transformed frames dataset
var betweenFrameApprox = function(frames, drop_count, drop_type) {
  var randomIndex, index;
  var indices = [];

  for (var i = 0; i < drop_count; i++) {
    do {
      randomIndex = Math.floor(Math.random() * (frames.length - 2)) + 1;
    } while (indices.indexOf(randomIndex) != -1);
    indices.push(randomIndex);
  }

  indices.sort(function(a, b) {
    return a - b;
  });

  for (var j = 0; j < indices.length; j++) {
    index = indices[j];
    if (drop_type == "copy")
      frames[index] = frames[index - 1];
    else if (drop_type == "interpolation")
      for (var k = 0; k < frames[index].length; k++) {
        frames[index][k].y = (frames[index - 1][k].y + frames[index + 1][k].y) / 2;
      }
  }

  return frames;
}

// Generates a power trend function (bar height changes exponentially over time)
// @param exp: Exponent of the power function
// @param max: Max height of highlighted bar as a percentage of bar chart height (eg. 0.18, 0.55)
// @param max_position: Frame which holds max height as a percentage of total frames (eg. 0, 0.5, 1)
// @param frames: Number of frames - 1
// @param noise: Standard deviation for random normal distribution
var powerTrend = function(exp, max, max_position, frames, noise) {
  var f = Math.floor(max_position * frames);
  var left = d3.scale.pow().domain([0, f]).range([0.05, max]).exponent(exp);
  var right = d3.scale.pow().domain([0, frames-f]).range([0.05, max]).exponent(exp);
  var fn = function(frame) {
    var result;
    if (frame < f) {
      var randLeft = d3.random.normal(left(frame), noise);
      do {
        result = randLeft();
      } while(result >= max || result < 0.05);
      return result;
    }
    if (frame == f) {
      return max;
    }
    var randRight = d3.random.normal(right(frames - frame), noise);
    do {
      result = randRight();
    } while(result >= max || result < 0.05);
    return result;
  }
  return fn;
}

// Randomly generates a dataset using power functions for the trend
// @param exp: Exponent of the power function
// @param max: Max height reached during animation
// @param max_position: Frame which holds the max height
// @param noise: Standard deviation for random distribution
// @param duration: Number of seconds to run the animation
// @param fps: Number of frames per second
// @param marking: Specifies highlight of bar, either "color" or "circle"
// @return JS object of data
var generatePowerChartData = function(exp, max, max_position, noise, duration, fps, marking) {
  var trendFn = powerTrend(exp,max,max_position,duration*fps-1,noise);
  var random = function(i) { return {x: i, y: Math.random() * (0.95 - 0.05) + 0.05}; };
  var gendata = function(i) {
    var group = d3.range(5).map(random);
    group[2].y = trendFn(i);
    return group;
  };
  if ( !((max_position == 0.5 && max == .85 && fps == 10) ||
       (exp == 10 && max_position == 0.5 && max == .85 && fps == 30) ||
       (exp == 10 && max_position < 0.5 && max == .85 && fps == 10) ||
       (exp == 10 && max_position == 0.5 && max == .22 && fps == 10))) return;
  var frames = d3.range(duration*fps).map(gendata);
  var exptype = (exp == 1)? 'Linear' : 'Exponential';

  var data = {};
  data['id'] = 'exp-' + exp + '-maxpos-' + max_position + '-max-' + (100 * max) + '-fps-' + fps;
  data['id'] = 'Max Value = ' + (100*max) + "%, Pos = " + (100*max_position) +
               "%, " + fps + " FPS, " + exptype; 
  data['type'] = "test";
  data['exponent'] = exp;
  data['fps'] = fps;
  data['max_frame'] = max_position;
  data['max'] = max;
  data['seed'] = seed;
  data['noise'] = noise;
  data['duration'] = duration;
  data['marking'] = marking;
  data['frames'] = frames;

  return data;
}

//generate the distractor with certain correlation with the target bar
var generateCorrPowerChartData = function(exp, max, max_position, noise, duration, fps, marking, corr, avg_num, init_noise) {
    var avgType = average_types[avg_num];
    var trendFn = powerTrend(exp,max,max_position,duration*fps-1,noise);
    var random = function(i) { return {x: i, y: Math.random() * (0.95 - 0.05) + 0.05}; };
    var init_target_h = trendFn(0);
    var init_random = function(i) {
    	if(i < avgType.min || i > avgType.max) return random(i);
    	else {
    		var distractor_h = (1 + init_noise) * init_target_h;
    		return {x: i, y: Math.max(Math.min(distractor_h, 0.95), 0.05)};
    	}
    };
    var inits = [];
    
    var gendata = function(i) {	
      var group = d3.range(5).map(random);
      if(i == 0){
    	  group = d3.range(5).map(init_random);
    	  inits = group;
    	  inits[2].y = init_target_h;
    	  return group;
      }
      var cur = trendFn(i);
      var delta = cur - inits[2].y;
      for(var j = avgType.min; j <= avgType.max; ++j){
    	  var y = corr * (delta + inits[j].y) + (1 - corr) * random(0).y;
    	  group[j].y = Math.max(Math.min(y, 0.95), 0.05); 
      }
      group[2].y = cur;
      return group;
    };
    var frames = d3.range(duration*fps).map(gendata);

    var data = {};
    data['id'] = 'exp-' + exp + '-maxpos-' + max_position + '-max-' + (100 * max) + "-corr-" + corr + "-init_noise-" + init_noise;
    data['type'] = "test";
    data['exponent'] = exp;
    data['fps'] = fps;
    data['max_frame'] = max_position;
    data['max'] = max;
    data['seed'] = seed;
    data['noise'] = noise;
    data['duration'] = duration;
    data['marking'] = marking;
    data['frames'] = frames;
    data['corr'] = corr;
    data['init_noise'] = init_noise;

    return data;
}

var average_types = [
     { min: 1, max: 2 },
     { min: 1, max: 3 },
     { min: 1, max: 4 }
   ];

var withinFrameApprox = function(frames, average_type) {
     var minIndex = average_types[average_type].min;
     var maxIndex = average_types[average_type].max
     for (var i = 0; i < frames.length; i++) {
       var sum = 0;
       for (var j = minIndex; j <= maxIndex; j++) {
         sum += frames[i][j].y;
       }
       var avg = sum / (maxIndex - minIndex + 1);
       for (var j = minIndex; j <= maxIndex; j++) {
         frames[i][j].y = avg;
       }
     }

     return frames;
}

var generateWithinFrameApprox = function() {
   var init_noises = [0.1, 0.2, 0.3];
   var exponents = [1, 5];
   var max_positions = [0.25, 0.75];
   var heights = [0.22, 0.32, 0.47, 0.69, 0.85];
   var fpss = [30];
   var noises = [0];
   var corrs = [0, 0.5, 0.65, 0.8, 1];
   var duration = 2;
   var marking = "color";
   var jsonData = [];
   var datum;

   for (var i = 0; i < fpss.length; i++) {
     for (var j = 0; j < exponents.length; j++) {
       for (var k = 0; k < max_positions.length; k++) {
         for (var l = 0; l < heights.length; l++) {
           for (var m = 0; m < noises.length; m++) {
             for (var n = 0; n < average_types.length; n++) {
	        	 for(var p = 0; p < corrs.length; p++){
	        		 for(var q = 0; q < init_noises.length; q++){
	        			 datum = generateCorrPowerChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking, corrs[p], n, init_noises[q]);
  		                 datum.frames = withinFrameApprox(datum.frames, n);
  		                 datum['id'] = datum['id'] + '-averageType-' + average_types[n].min + ',' + average_types[n].max;
  		                 datum['average_type_index'] = n;
  		                 datum['average_type'] = average_types[n];
  		                 jsonData.push(datum); 
	        		 } 
	        	 }
             }
           }
         }
       }
     }
   }
   return jsonData;
}

function sampleNoiseDataset(array) {
    var result = [];
    var tasks = {}
    for (var i = 0; i < array.length; i++) {
      var task = array[i];
      if (tasks[task.exponent] == undefined) {
        tasks[task.exponent] = {};
        tasks[task.exponent][task.max_frame] = {};
        tasks[task.exponent][task.max_frame][task.noise] = [];
      }
      else if (tasks[task.exponent][task.max_frame] == undefined) {
        tasks[task.exponent][task.max_frame] = {};
        tasks[task.exponent][task.max_frame][task.noise] = [];
      }
      else if (tasks[task.exponent][task.max_frame][task.noise] == undefined) {
        tasks[task.exponent][task.max_frame][task.noise] = [];
      }
      tasks[task.exponent][task.max_frame][task.noise].push(task);
    }

    for (var exponent in tasks) {
      for (var max_frame in tasks[exponent]) {
        for (var noise in tasks[exponent][max_frame]) {
          var arr = shuffle(tasks[exponent][max_frame][noise], 0);
          result.push(arr[0]);
          result.push(arr[1]);
          result.push(arr[2]);
        }
      }
    }

    return result;
}

var relativeNoiseTrend = function(exp, max, max_position, frames, noise) {
    var f = Math.floor(max_position * frames);
    var left = d3.scale.pow().domain([0, f]).range([0.05, max]).exponent(exp);
    var right = d3.scale.pow().domain([0, frames-f]).range([0.05, max]).exponent(exp);
    var uniformRand = function(height) {
      return Math.random() * (((1+noise)*height) - ((1-noise)*height)) + ((1-noise)*height);
    };
    var fn = function(frame) {
      var result;
      if (frame < f) {
        do {
          result = uniformRand(left(frame));
        } while(result >= max || result < 0.05);
        return result;
      }
      if (frame == f) {
        return max;
      }
      do {
        result = uniformRand(right(frames - frame));
      } while(result >= max || result < 0.05);
      return result;
    }
    return fn;
  }


var generatePowerRelativeNoiseChartData = function(exp, max, max_position, noise, duration, fps, marking) {
    var trendFn = relativeNoiseTrend(exp,max,max_position,duration*fps-1,noise);
    var random = function(i) { return {x: i, y: Math.random() * (0.95 - 0.05) + 0.05}; };
    var gendata = function(i) {
      var group = d3.range(5).map(random);
      group[2].y = trendFn(i);
      return group;
    };
    var frames = d3.range(duration*fps).map(gendata);

    var data = {};
    data['id'] = 'exp-' + exp + '-max-' + (100 * max) + '-noise-' + noise;
    data['type'] = "test";
    data['exponent'] = exp;
    data['fps'] = fps;
    data['max_frame'] = max_position;
    data['max'] = max;
    data['seed'] = seed;
    data['noise'] = noise;
    data['duration'] = duration;
    data['marking'] = marking;
    data['frames'] = frames;

    return data;
}

var generateDataset = function() {
    var exponents = [1, 5, 10];
    var max_positions = [0.25, 0.5, 0.75];
    var heights = [0.22, 0.32, 0.47, 0.69, 0.85];
    var fpss = [30];
    var noises = [0, 0.1, 0.2, 0.3, 0.5];
    var duration = 5;
    var marking = "color";
    var jsonData = [];
    var datum;

    for (var i = 0; i < fpss.length; i++) {
      for (var j = 0; j < exponents.length; j++) {
        for (var k = 0; k < max_positions.length; k++) {
          for (var l = 0; l < heights.length; l++) {
            for (var m = 0; m < noises.length; m++) {
              datum = generatePowerRelativeNoiseChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking);
              jsonData.push(datum);
            }
          }
        }
      }
    }

    return jsonData;
}

var generateDataset = function() {
    var exponents = [1, 10];
    var max_positions = [0.25, 0.5, 0.75];
    var heights = [0.22,  0.85];
    var fpss = [10, 30];
    var noises = [0]; //, 0.1, 0.2, 0.3, 0.5];
    var drops = [0, .5, .8];
    var duration = 2;
    var marking = "color";
    var jsonData = [];
    var datum;

    for (var i = 0; i < fpss.length; i++) {
      for (var j = 0; j < exponents.length; j++) {
        for (var k = 0; k < max_positions.length; k++) {
          for (var l = 0; l < heights.length; l++) {
            for (var m = 0; m < noises.length; m++) {
              for (var d = 0; d < drops.length; d++) {
                //datum = generatePowerRelativeNoiseChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking);
                datum = generatePowerChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking);
                if (!datum) continue;
                datum.frames = betweenFrameApprox(datum.frames, duration * fpss[i] * drops[d], 'interpolation');
                datum.id = datum.id + '-' + drops[d];
                if (datum) jsonData.push(datum);
              }
            }
          }
        }
      }
    }

    return jsonData;
  }

// Fisher-Yates shuffle
function shuffle(array, minIndex) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (minIndex !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * (currentIndex - minIndex)) + minIndex;
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

function sampleDataset(array) {
    var result = [];
    var tasks = {}
    for (var i = 0; i < array.length; i++) {
      var task = array[i];
      if (tasks[task.init_noise] == undefined) {
        tasks[task.init_noise] = {};
        tasks[task.init_noise][task.corr] = {};
        tasks[task.init_noise][task.corr][task.average_type_index] = [];
      }
      else if (tasks[task.init_noise][task.corr] == undefined) {
        tasks[task.init_noise][task.corr] = {};
        tasks[task.init_noise][task.corr][task.average_type_index] = [];
      }
      else if (tasks[task.init_noise][task.corr][task.average_type_index] == undefined) {
        tasks[task.init_noise][task.corr][task.average_type_index] = [];
      }
      tasks[task.init_noise][task.corr][task.average_type_index].push(task);
    }

    for (var init_noise in tasks) {
      for (var corr in tasks[init_noise]) {
        for (var average_type_index in tasks[init_noise][corr]) {
          var arr = shuffle(tasks[init_noise][corr][average_type_index], 0);
          result.push(arr[0]);
          result.push(arr[1]);
          result.push(arr[2]);
        }
      }
    }

    return result;
  }

/*for (var i = 0; i < fpss.length; i++) {
  for (var j = 0; j < exponents.length; j++) {
    for (var k = 0; k < max_positions.length; k++) {
      for (var l = 0; l < heights.length; l++) {
        for (var m = 0; m < noises.length; m++) {
          for (var n = 0; n < drop_percents.length; n++) {
            seedrandom(seed, { global: true });
            //datum = generatePowerChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking);
            datum = generatePowerChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking, 0.8);
            datum.frames = betweenFrameApprox(datum.frames, duration * fpss[i] * drop_percents[n], drop_type);
            datum['id'] = datum['id'] + '-dropPercent-' + drop_percents[n];
            datum['drop_type'] = 'between-frame-copy';
            datum['drop_percent'] = drop_percents[n];
            jsonData.push(datum);
          }
        }
      }
    }
  }
}*/

dataset = generateDataset();
console.log(dataset.length);
sample = sampleNoiseDataset(dataset);
console.log(sample.length);
//dataset = sampleDataset();
//console.log(dataset);

var outputFilename = './paper_animated_examples.json';
fs.writeFile(outputFilename, JSON.stringify(dataset, null, "  "), function(err) {
	if(err) {
		console.log(err);
	} else {
		console.log(outputFilename);
		console.log("JSON saved to " + outputFilename);
	}
});