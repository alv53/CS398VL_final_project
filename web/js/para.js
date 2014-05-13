function main(data){
  var margin = {top: 60, right: 20, bottom: 50, left: 100},
      width = 1000 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var x = d3.scale.linear()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .tickValues([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var yBar = d3.svg.line()
      .x(10)
      .y(30);
 
  var line = d3.svg.line()
      .x(function(d) { return x(d.pos); })
      .y(function(d) { return y(d.sentiment); });


    var posArea = d3.svg.area()
        .x(function(d) { return x(d.pos); })
        .y0(height/2) 
        // .y1(function(d) { return y(d.sentiment); });
        .y1(function(d) { return (y(d.sentiment) < height/2 ? y(d.sentiment) : height/2); });

  var negArea = d3.svg.area()
      .x(function(d) { return x(d.pos); })
      .y0(height/2)
      .y1(function(d) { return (y(d.sentiment) > height/2 ? y(d.sentiment) : height/2); });

  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.tsv(data, function(error, data) {
    data.forEach(function(d) {
      d.pos = d.pos;
      d.sentiment = +d.sentiment;
    });

    x.domain([1, 1095]);
    y.domain([-100,100]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
      .append("text")
        .text("Paragraph")
        .style("text-anchor", "end")
        .attr("y", 30)
        .attr("x", 100+width/2)
        .attr("dy", ".71em");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -70)
        .attr("x", 30-height/2)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Sentiment");

    svg.append("g")
        .attr("class", "y bar")
        .call(yBar);

    // svg.append("path")
    //     .datum(data)
    //     .attr("class", "line")
    //     .attr("d", line);

    svg.append("path")
        .datum(data)
        .attr("class", "posArea")
        .attr("d", posArea);

    svg.append("path")
        .datum(data)
        .attr("class", "negArea")
        .attr("d", negArea);

    svg.append("line")
        .attr("x1", 0.227397260274*width)
        .attr("y1", -40)
        .attr("x2", 0.227397260274*width)
        .attr("y2", -5)
        .attr("class", "partSplitter");
    
    svg.append("line")
        .attr("x1", 0.358904109589*width)
        .attr("y1", -40)
        .attr("x2", 0.358904109589*width)
        .attr("y2", -5)
        .attr("class", "partSplitter");

    svg.append("line")
        .attr("x1", 0.504109589041*width)
        .attr("y1", -40)
        .attr("x2", 0.504109589041*width)
        .attr("y2", -5)
        .attr("class", "partSplitter");

    svg.append("line")
        .attr("x1", 0.785388127854*width)
        .attr("y1", -40)
        .attr("x2", 0.785388127854*width)
        .attr("y2", -5)
        .attr("class", "partSplitter");    

    svg.append("line")
        .attr("x1", 0)
        .attr("x2", width)
        .attr("y1", height/2)
        .attr("y2", height/2)
        .attr("class", "origin");
  });  
}
