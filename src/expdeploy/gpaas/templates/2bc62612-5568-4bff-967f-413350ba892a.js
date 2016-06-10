var d3 = require("d3")
var Regex = require("regex");
var seed = 'perceptvis';		//TODO: need to change this

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

var generatePowerChartData = function(exp, max, max_position, noise, duration, fps, marking) {
    var trendFn = powerTrend(exp,max,max_position,duration*fps-1,noise);
    var random = function(i) { return {x: i, y: Math.random() * (0.95 - 0.05) + 0.05}; };
    var gendata = function(i) {
      var group = d3.range(5).map(random);
      group[2].y = trendFn(i);
      return group;
    };
    var frames = d3.range(duration*fps).map(gendata);

    var data = {};
    data['id'] = 'exp-' + exp + '-maxpos-' + max_position + '-max-' + (100 * max);
    data['rel_max'] = 100 * max
    data['rel_exp'] = exp
    data['rel_maxpos'] = max_position
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

var betweenFrameApprox = function(frames, drop_count, drop_type) {
    var randomIndex, index;
    var indices = [];
    var linear = function (m, b) {
      var f = function(x) {
        return m * x + b;
      };
      return f;
    };

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
      else if (drop_type == "interpolation") {
        var firstIndex = index;
        while (j < indices.length - 1 && indices[j+1] == indices[j] + 1)
          j++;
        var lastIndex = indices[j];
        // interpolate between firstIndex - 1 and lastIndex + 1
        for (var k = 0; k < frames[index].length; k++) {
          var m = (frames[lastIndex+1][k].y - frames[firstIndex-1][k].y) / (lastIndex - firstIndex + 2);
          var b = frames[firstIndex-1][k].y;
          var s = linear(m, b);
          for (var l = 1; l <= lastIndex - firstIndex + 1; l++) {
            frames[firstIndex + l - 1][k].y = s(l);
          }
        }
      }
    }

    return frames;
}
 
 var generateBetweenFrameApprox = function() {
	 var exponents = [1, 5, 10];
	 var max_positions = [0, 0.25, 1];
	 var heights = [0.22, 0.32, 0.47, 0.69, 0.85];
	 var fpss = [30];
	 var noises = [0];
	 var duration = 2;
	 var marking = "color";
	 var drop_type = "copy";
	 var drop_percents = [0, 0.2, 0.4, 0.6, 0.8];
	 var jsonData = [];
	 var datum;
	
	 for (var i = 0; i < fpss.length; i++) {
	   for (var j = 0; j < exponents.length; j++) {
	     for (var k = 0; k < max_positions.length; k++) {
	       for (var l = 0; l < heights.length; l++) {
	         for (var m = 0; m < noises.length; m++) {
	           for (var n = 0; n < drop_percents.length; n++) {
	             //datum = generatePowerChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking);
	             datum.frames = betweenFrameApprox(datum.frames, duration * fpss[i] * drop_percents[n], drop_type);
	             datum['id'] = datum['id'] + '-dropPercent-' + drop_percents[n];
	             datum['drop_type'] = 'between-frame-' + drop_type;
	             datum['drop_percent'] = drop_percents[n];
                 jsonData.push(datum);
               }
             }
           }
         }
       }
     }

	 return jsonData;
}

 var average_types = [
                      { min: 2, max: 2 },
                      { min: 1, max: 2 },
                      { min: 2, max: 3 },
                      { min: 1, max: 3 },
                      { min: 0, max: 3 },
                      { min: 1, max: 4 },
                      { min: 0, max: 4 }]; 
 
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
	 var exponents = [1, 5, 10];
	 var max_positions = [0, 0.25, 1];
	 var heights = [0.22, 0.32, 0.47, 0.69, 0.85];
	 var fpss = [30];
	 var noises = [0];
	 var duration = 2;
	 var marking = "color";
	 var average_types_count = 7;
	 var jsonData = [];
	 var datum;
	
	 for (var i = 0; i < fpss.length; i++) {
	   for (var j = 0; j < exponents.length; j++) {
	     for (var k = 0; k < max_positions.length; k++) {
	       for (var l = 0; l < heights.length; l++) {
	         for (var m = 0; m < noises.length; m++) {
	           for (var n = 0; n < average_types_count; n++) {
	             datum = generatePowerChartData(exponents[j], heights[l], max_positions[k], noises[m], duration, fpss[i], marking);
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
	 return jsonData;
}

function sampleDataset(array) {
    var result = [];
    var tasks = {}
    for (var i = 0; i < array.length; i++) {
      var task = array[i];
      if (tasks[task.exponent] == undefined) {
        tasks[task.exponent] = {};
        tasks[task.exponent][task.max_frame] = {};
        tasks[task.exponent][task.max_frame][task.average_type_index] = [];
      }
      else if (tasks[task.exponent][task.max_frame] == undefined) {
        tasks[task.exponent][task.max_frame] = {};
        tasks[task.exponent][task.max_frame][task.average_type_index] = [];
      }
      else if (tasks[task.exponent][task.max_frame][task.average_type_index] == undefined) {
        tasks[task.exponent][task.max_frame][task.average_type_index] = [];
      }
      tasks[task.exponent][task.max_frame][task.average_type_index].push(task);
    }

    for (var exp in tasks) {
      for (var max_frame in tasks[exp]) {
        for (var average_type_index in tasks[exp][max_frame]) {
          var arr = shuffle(tasks[exp][max_frame][average_type_index], 0);
          result.push(arr[0]);
          result.push(arr[1]);
        }
      }
    }

    return result;
  }

//Fisher-Yates shuffle
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

var charTable = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
var workerIdSet = {}

function getWorkerIdLength(){
	var minLen = 10;
	var maxLen = 15;
	return Math.floor(Math.random() * (maxLen - minLen) + minLen)
}

function getWorkerId(){
	var n = getWorkerIdLength()
	var workerId = ""
	do {
		for(var i = 0; i < n; ++i){
			var randomIndex = Math.floor(Math.random() * 36) 
			workerId += charTable[randomIndex]
		}
	} while(workerIdSet[workerId]);	
	workerIdSet[workerId] = true
	return workerId;
}

var ss = require('simple-statistics')
var taskIndex = 0;
var simulationTimes = 10
var maxPattern = new Regex(/max-\d+/);
var numPattern = new Regex(/\d+/)
var corrSum = 0
var minCorr = 1.0, maxCorr = -1;

for(var i = 0; i < simulationTimes; ++i){
	seed = getWorkerId()
	console.log(seed)
	var dataset = generateWithinFrameApprox();
	dataset = sampleDataset(dataset);
	var maxes = dataset.map(function(datum){ return datum['rel_max'];})
	var randomMaxes = dataset.map(function(datum){ return Math.floor(Math.random() * 100 + 1);})
	var corr = ss.sampleCorrelation(maxes, randomMaxes)
	//console.log(maxes)
	//console.log(randomMaxes)
	corrSum += corr
	if(corr > maxCorr) maxCorr = corr
	if(corr < minCorr) minCorr = corr
	var line = i + "\t corr:" + corr + "\t minCorr:" + minCorr + "\t maxCorr:" + maxCorr + "\t threshold:" + (corrSum / (i + 1)) 
	console.log(line)
}
console.log(corrSum / simulationTimes)