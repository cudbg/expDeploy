import "planout";
import "extend";

var experimentName = "";


function setExperiment(name) {
	experimentName = name;


}

function setup(callback) {
	window.addEventListener("load", callback);
}

/*

 options = {
  "n":Number, // the number of parameters you want to receive
  "userId": String, //the user id to be hashed
  "saveProgress":true //whether to query the server 
 }

*/
function getParameters(userid, options) {
	params = []


	var n = 1
	var id = Math.round(Math.random()*1000000);

	if (options["n"]) {
		n = options["n"];
	}
	if (options["userId"]) {
		id = options["userId"];
	}


	/*

		TODO: Send HTTP request to server, check to see if USERID has been used before

		if it has: return the parameters that were saved before
		else: do the code below to generate new parameters, and save them to the server
	*/

	for (i = 0; i < n; i++) {
		
		var exp = new window[experimentName]({userId:(id + i)});

		names = exp.getParamNames();

		for (j=0; j < names.length; j++) {
			exp.get(names[j]);
		}


        params[i] = exp._assignment._data;

	}



	return params;
}

