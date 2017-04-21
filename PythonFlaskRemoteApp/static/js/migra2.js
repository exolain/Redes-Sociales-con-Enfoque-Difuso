var app=angular.module('myApp', []);
app.controller('HomeCtrl', function($scope, $http) {
	
		$scope.info = {};
		
		$scope.showAdd = true;

$scope.showlist = function() {
    $http({
        method: 'POST',
        url: '/getMoveList',

    }).then(function(response) {
        $scope.moves = response.data;
        console.log('mm', $scope.moves);
    }, function(error) {
        console.log(error);
    });
}

$scope.showList

var width = 960;
var height = 700;
  var formatC = d3.format(",.0f");
  var formatD = d3.format("+,.0f");

   var immin, immax, exmin, exmax;
    var colors = ["#EDF8FB","#41083e"];
  var immdomain = [24431,537148];
  var emmdomain = [20056,566986];
  
  var circleSize = d3.scale.linear().range([0,25000]).domain([0, 137175]);

  var lineSize = d3.scale.linear().range([2,25]).domain([0, 35000]);

  var fillcolor = d3.scale.linear().range(colors).domain(immdomain);

var projection = d3.geo.mercator()
.scale(12000)
.center([-84.5, 10.1]);

var path = d3.geo.path()
.projection(projection);

var svg = d3.select("body").append("svg")
.attr("width", width)
.attr("height", height);

var formatNumber = d3.format(",.0f");

var radius = d3.scale.sqrt()
	.domain([0, 1e6])
	.range([0, 15]);


var legend = svg.append("g")
	.attr("class", "legend")
	.attr("transform", "translate(" + (width - 50) + "," + (height - 20) + ")")
	.selectAll("g")
	.data([1e6, 5e6, 1e7])
	.enter().append("g");

legend.append("circle")
	.attr("cy", function(d) { return -radius(d); })
	.attr("r", radius);

legend.append("text")
	.attr("y", function(d) { return -2 * radius(d); })
	.attr("dy", "1.3em")
	.text(d3.format(".1s"));


	
d3.json("static/js/regionescr.topojson", function(error, topology, $scope) {
//	var regiones=topojson.object(topology, topology.objects.collection);
	svg.append("g")
	.attr("class", "provincia-boundary")
	.selectAll("path")
	.data(topojson.feature(topology, topology.objects.collection).features)
	.enter().append("path")
	.attr("d", path)	
	.text(function(d) { return d.properties.Name; });	
//	.style("fill", function(d) { return fill(path.area(d)); });
	
	svg.append("path")
	.datum(topojson.mesh(topology, topology.objects.collection, function(a, b) { return a !== b; }))
	.attr("d", path)
	.attr("class", "provincia-boundary");

//console.log("hey"+moveList);
/*var geometries = topojson.object(topology, topology.objects.collection.geometries);

for (var i = 0; i < moveList.length; i++) {
    for (var j = 0; j < geometries.length; j++) {
        if (moveList[i].in == geometries[j].id) {
            geometries[j].properties.count = moveList[i].count;
        }
    }
}	
    svg.selectAll("path")
	.data(regiones.geometries)
	.append("svg:title")
	.attr("class", function(d) { return "path " + d.id; })
	.attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
	.attr("dy", ".35em")
	.text(function(d) { return d.properties.Name; });
*/
features=topojson.feature(topology, topology.objects.collection).features;
		//Find the corresponding state inside the GeoJSON
		for (var j = 0; j < features.length; j++) {
		  var jsonState = features[j].properties.name;
		  var tempObj = {};
		  //if (dataName == jsonState) {
		  
			matched = true;
			features[j].properties.state = jsonState;
			features[j].id = jsonState;
			

			for (var propt in tempObj) {
				if(!isNaN(tempObj[propt])) {
			  topology.features[j].properties[propt] = tempObj[propt];
			  }

			}
			//break;
		//  }
		}
	  

	
	  //Bind data and create one path per GeoJSON feature
	  svg.selectAll("path")
		.data(features)
		.enter()
		.append("path")
		.attr("class", "state")
		.attr("id", function(d) {
			return d.properties.state;
			})
		.attr("d", path)
		.attr("stroke-width", 0.5)
		.style("stroke", "#666")
		.style("fill", "#fff");
  			 
	   svg.selectAll("circle")
	.data(features)
	.enter().append("circle")
	.attr("cx", function(d) {
		var centname = d.properties.name;
		var ctroid;
		ctroid = path.centroid(d)[0];
		return ctroid;
	})
	.attr("cy", function(d) {
		var centname = d.properties.name;
		var ctroid;
		ctroid = path.centroid(d)[1];
		return ctroid;
	})
	.attr("r", function(d) {
		var diff = 10-5;// d.properties.total_imm - d.properties.total_emm;
		return circleSize(Math.sqrt(Math.abs(diff)/Math.PI));
	
	})
	.attr("class", "circ")
	.attr("id", function(d) {return d.abbrev;})
	.attr("fill", function(d) {
		var diff = 11-5 //d.properties.total_imm - d.properties.total_emm;
		if(diff>0) {
		return "#65a89d";
		} else {
		return "#a96a46";
		}
	
	})
	.attr("fill-opacity", "0.5")
	.attr("stroke", "#fff")
	.attr("stroke-weight", "0.5")
	
		
		.on("mouseover", function (d) {
		  return toolOver(d, this);
		})
		.on("mousemove", function (d) {
		  var m = d3.mouse(this);
		  mx = m[0];
		  my = m[1];
		  return toolMove(mx, my, d);
		})
		.on("mouseout", function (d) {
		  return toolOut(d, this);
		})
	.on("click", function(d) {clicked(d)});

		
  });
});

function toolOver(v, thepath) {

	d3.select(thepath).style({
		"fill-opacity": "0.7",
		"cursor":"pointer"
	});
	return tooltip.style("visibility", "visible");
};

function toolOut(m, thepath) {
	d3.select(thepath).style({
		"fill-opacity": "0.5",
		"cursor":""
	});
	return tooltip.style("visibility", "hidden");
};


function toolMove(mx, my, data) {

	if (mx < 120) {
		mx = 120
	};
	
		if (my < 40) {
		my = 40
	};
	return tooltip.style("top", my + -140 + "px").style("left", mx - 120 + "px").html("<div id='tipContainer'><div id='tipLocation'><b>" + data.id + "</b></div><div id='tipKey'>Migration in: <b>" + formatC(data.properties.total_imm) + "</b><br>Migration out: <b>" + formatC(data.properties.total_emm) + "</b><br>Net migration: <b>" + formatC((data.properties.total_imm - data.properties.total_emm)) + "</b></div><div class='tipClear'></div> </div>");
};

function toolOver2(v, thepath) {

	d3.select(thepath).style({
		"opacity": "1",
		"cursor":"pointer"
	});
	return tooltip2.style("visibility", "visible");
};

function toolOut2(m, thepath) {
	d3.select(thepath).style({
		"opacity": "0.5",
		"cursor":""
	});
	return tooltip2.style("visibility", "hidden");
};

function toolMove2(mx, my, home, end, v1, v2) {
var diff = v1-v2;

	if (mx < 120) {
		mx = 120
	};
	
		if (my < 40) {
		my = 40
	};
	return tooltip2.style("top", my + -140 + "px").style("left", mx - 120 + "px").html("<div id='tipContainer2'><div id='tipLocation'><b>" + home + "/" + end + "</b></div><div id='tipKey2'>Migration, " + home + " to " + end +": <b>" + formatC(v2) + "</b><br>Migration, " + end + " to " + home +": <b>" + formatC(v1)+ "</b><br>Net change, " + home + ": <b>" + formatD(v1-v2) + "</b></div><div class='tipClear'></div> </div>");
};

  
  function clicked(selected) {
  //var coming = selected.properties;
  var selname = selected.id;

/*
	d3.selectAll(".circ")
	.attr("fill-opacity", "0.2");
*/
  
  var homex = path.centroid(selected)[0];
  var homey = path.centroid(selected)[1];

  g.selectAll(".goingline")
  .attr("stroke-dasharray", 0)
  .remove()
  
  
  g.selectAll(".goingline")
  .data(going)
  .enter().append("path")
  .attr("class", "goingline")
  
  .attr("d", function(d,i) 
  	{
 	//console.log(coming[i][selname], coming[i].state);
 	//console.log(going[i][selname], going[i].state);
  	var abb = d.abbrev;
  	var finalval = coming[i][selname] - going[i][selname];
  	
  	
  	var theState = d3.select("#" + abb);
  	
	if(!isNaN(finalval)) {
  	var startx = path.centroid(theState[0][0].__data__)[0];
  	var starty = path.centroid(theState[0][0].__data__)[1];

  	  if(finalval > 0) {
  	    	  	return "M" + startx + "," + starty + " Q" + (startx + homex)/2 + " " + (starty + homey)/1.5 +" " + homex+" "   + homey;

  	} else {
  	  	return "M" + homex + "," + homey + " Q" + (startx + homex)/2 + " " + (starty + homey)/2.5 +" " + startx+" "   + starty;
  	}
  	}
  	})
  	
  .call(transition)

  .attr("stroke-width", function(d,i) {
	var finalval = coming[i][selname] - going[i][selname];
	
  	return lineSize(parseFloat(Math.abs(finalval)));
  	})
  .attr("stroke", function(d,i) {
  var finalval = coming[i][selname] - going[i][selname];
  if(finalval > 0) {
  
  return "#65a89d";
  } else {
  return "#a96a46";
  }
  
  })
  .attr("fill", "none")
  .attr("opacity", 0.5)
  .attr("stroke-linecap", "round")
  .on("mouseover", function (d) {
		  return toolOver2(d, this);
		})
		.on("mousemove", function (d,i) {
		  var m = d3.mouse(this);
		  mx = m[0];
		  my = m[1];
		  return toolMove2(mx, my, selname, d.state, coming[i][selname], going[i][selname]);
		})
		.on("mouseout", function (d) {
		  return toolOut2(d, this);
		});

  
  }
  
  
function transition(path) {
  path.transition()
      .duration(1500)
      .attrTween("stroke-dasharray", tweenDash);
}

function tweenDash() {
  var l = this.getTotalLength(),
      i = d3.interpolateString("0," + l, l + "," + l);
  return function(t) { return i(t); };
}
