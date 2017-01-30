

       angular.module('myApp', [])
            .controller('HomeCtrl', function($scope, $http) {
			
			//	$scope.info = {};
				
			//	$scope.showAdd = true;
		var width = 960;
		var height = 700;

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


			

		d3.json("static/js/map.topojson", function(error, topology) {
		  
		svg.append("path")
		.datum(topojson.mesh(topology, topology.objects.collection, function(a, b) { return a !== b; }))
		.attr("d", path)
		.attr("class", "provincia-boundary");

		svg.append("g")
			.attr("class", "bubble")
			.selectAll("circle")
			.data(topojson.feature(topology, topology.objects.collection).features
			.sort(function(a, b) { return b.properties.population - a.properties.population; }))
			.enter().append("circle")
			.attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
			.attr("r", function(d) { return radius(d.properties.population); }) 
			.append("title")
			.text(function(d) {
			return d.properties.name
				+ "\nPopulation " + formatNumber(d.properties.population);
      });

        });

            });
