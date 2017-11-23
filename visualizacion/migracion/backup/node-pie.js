
var DEFAULT_OPTIONS = {
    radius: 20,
    outerStrokeWidth: 10,
    parentNodeColor: 'transparent',
    showPieChartBorder: true,
    pieChartBorderColor: 'white',
    pieChartChildBorderColor: 'white',
    pieChartBorderWidth: '4',
    showLabelText: false,
    labelText: 'text',
    cx:0,
    cy:0,
    labelColor: 'blue'
};

function getOptionOrDefault(key, options, defaultOptions) {
    defaultOptions = defaultOptions || DEFAULT_OPTIONS;
    if (options && key in options) {
        return options[key];
    }
    return defaultOptions[key];
}

function drawParentCircle(nodeElement, options) {
    var outerStrokeWidth = getOptionOrDefault('outerStrokeWidth', options);
    var radius = getOptionOrDefault('radius', options);
    var parentNodeColor = getOptionOrDefault('parentNodeColor', options);

    nodeElement.insert("circle")
        .attr("id", "parent-pie")
        .attr("r", radius)
        .attr("fill", function (d) {
            return parentNodeColor;
        })
        .attr("stroke", function (d) {
            return parentNodeColor;
        })
        .attr("stroke-width", outerStrokeWidth);
}

function drawPieChartBorder(nodeElement, options) {
    var radius = getOptionOrDefault('radius', options);
    var pieChartBorderColor = getOptionOrDefault('pieChartBorderColor', options);
    var pieChartBorderWidth = getOptionOrDefault('pieChartBorderWidth', options);

    nodeElement.insert("circle")
        .attr("r", radius)
        .attr("fill", 'transparent')
        .attr("stroke", pieChartBorderColor)
        .attr("stroke-width", pieChartBorderWidth);
}

function drawPieChart(nodeElement, percentages, options) {
    var radius = getOptionOrDefault('radius', options);
    var cx = getOptionOrDefault('cx', options);
    var cy = getOptionOrDefault('cy', options);
    var pieChartChildBorderColor = getOptionOrDefault('pieChartChildBorderColor', options);
    var pieChartBorderWidth = getOptionOrDefault('pieChartBorderWidth', options);
    var halfRadius = radius / 2;
    var halfCircumference = 2 * Math.PI * halfRadius;
    color = d3.scale.category10();
    
    var percentToDraw = 0;
    for (var p in percentages) {
        var color_arc = 1;
        percentToDraw += percentages[p].percent;
        newcirc = nodeElement.insert('circle', '#parent-pie + *')
            .attr("r", halfRadius)
            .attr("fill", 'transparent')
            .attr("class", "children")
            .style('stroke', color(color_arc))
            .style('stroke-width', radius)
            .attr("transform", function(d) { return "translate(" + radius +","+ radius+ ")"; })
            .style('stroke-width', radius)
            .attr("cx", function (d) {
                        return cx;
                    })
                    .attr("cy", function (d) {
                        return cy; 
                    })
            .style('stroke-dasharray',
                    halfCircumference * percentToDraw / 100
                    + ' '
                    + halfCircumference);

        nodeElement.append("circle")
        .attr("r", radius)
        .attr("fill", 'transparent')
        .attr("transform", function(d) { return "translate(" + radius +","+ radius+ ")"; })
        .attr("cx", function (d) {
            return cx;
        })
        .attr("cy", function (d) {
            return cy; 
        })
        .attr("stroke", pieChartChildBorderColor)
        .attr("stroke-width", pieChartBorderWidth);

        color_arc++;
    }
}

function drawTitleText(nodeElement, options) {
    var radius = getOptionOrDefault('radius', options);
    var text = getOptionOrDefault('labelText', options);
    var color = getOptionOrDefault('labelColor', options);
        nodeElement.append("text")
            .text(String(text))
            .attr("fill", color)
            .attr("dy", radius * 2);
    
}

var NodePieBuilder = {
    drawNodePie: function (nodeElement, percentages, options) {
        drawParentCircle(nodeElement, options);
        if (!percentages) return;
        drawPieChart(nodeElement, percentages, options);

        var showPieChartBorder = getOptionOrDefault('showPieChartBorder', options);
        if (showPieChartBorder) {
            drawPieChartBorder(nodeElement, options);
        }

        var showLabelText = getOptionOrDefault('showLabelText', options);
        if (showLabelText ) {
            drawTitleText(nodeElement, options);
        }
    }
};