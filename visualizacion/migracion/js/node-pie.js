var DEFAULT_OPTIONS = {
    radius: 20,
    outerStrokeWidth: 10,
    classo: "children",
    parentNodeColor: 'blue',
    showPieChartBorder: true,
    pieChartBorderColor: 'white',
    pieChartBorderWidth: '2',
    showLabelText: false,
    labelText: 'text',
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
    var halfRadius = radius / 2;
    var halfCircumference = 2 * Math.PI * halfRadius;
    var classo = getOptionOrDefault('classo', options);

    var percentToDraw = 0;
    var color_arc =0;
    var range = ["#bcbddc", "#9e9ac8", "#756bb1", "#54278f"];
    //var range = ["#FF7100","#1a9850", "#1A5FFF","#FFD500"];

    for (var p in percentages) {
        percentToDraw += percentages[p].percent;
        if(percentToDraw >= 0.95) percentToDraw = 1;
        nodeElement.insert('circle', '#parent-pie + *')
            .attr("r", halfRadius)
            .attr("fill", 'transparent')
            .attr("class", classo)
            //.style('stroke', color(percentages[p].color))
            .style('stroke', range[color_arc])
            .style('stroke-width', radius)
            .style('stroke-dasharray',
                    halfCircumference * percentToDraw  // / 100
                    + ' '
                    + halfCircumference);

            color_arc++;

        if(percentToDraw == 1 ) break; 
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
        if (showLabelText) {
            drawTitleText(nodeElement, options);
        }
    }
};
