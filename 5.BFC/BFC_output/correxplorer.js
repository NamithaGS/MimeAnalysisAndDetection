var stringify = function (x) {
  if (typeof(x) === 'number' || x === undefined) {
    return String(x);
    // otherwise it won't work for:
    // NaN, Infinity, undefined
  } else {
    return JSON.stringify(x);
  }
};
$(document).ready(function(){

  $("a").on("click", function() {
      loadCSV(parseInt($(this).attr("identi")));
  });
  
  
  var loadCSV = function(i){
  
   var files = ["text_plain-correlationmatrix.csv","text_html-correlationmatrix.csv","image_gif-correlationmatrix.csv","image_jpeg-correlationmatrix.csv","audio_mpeg-correlationmatrix.csv","application_pdf-correlationmatrix.csv","application_msword-correlationmatrix.csv","application_vnd.ms-excel-correlationmatrix.csv","application_zip-correlationmatrix.csv","image_tiff-correlationmatrix.csv","application_octet-stream-correlationmatrix.csv","audio_x-ms-wma-correlationmatrix.csv","video_quicktime-correlationmatrix.csv","application_java-vm-correlationmatrix.csv","application_vnd.ms-powerpoint-correlationmatrix.csv","application_postscript-correlationmatrix.csv","application_atom+xml-correlationmatrix.csv","application_rdf+xml-correlationmatrix.csv","application_rss+xml-correlationmatrix.csv"];
  $('#filetype').text( files[i]);
    d3.csv(files[i], function(data){
      // I de-dictionatize d3 stuff
      // as of now assumes both columns and row labels
      var label_col_full = Object.keys(data[0]);
      var label_row = [];
      var rows = [];
      var row = [];
      for(var i = 0; i < data.length; i++){
        label_row.push(data[i][label_col_full[0]]);
        row = [];
        for(var j = 1; j < label_col_full.length; j++){
          row.push(parseFloat(data[i][label_col_full[j]]));
        }
        rows.push(row);
      }
      d3.select("svg").remove();

         main(rows, label_col_full.slice(1), label_row);
      
    });
  };


var main = function(corr, label_col, label_row){

  var transition_time = 1500;

  var body = d3.select('body');

  var tooltip = body.select('div.tooltip');
//    .style("opacity", 1e-6);

  var svg = body.append('svg')
    .attr('width', 3400)
    .attr('height', 3400);

  var sort_process = "value";
  

  var row = corr;
  var col = d3.transpose(corr);


  // converts a matrix into a sparse-like entries
  // maybe 'expensive' for large matrices, but helps keeping code clean
  var indexify = function(mat){
      var res = [];
      for(var i = 0; i < mat.length; i++){
          for(var j = 0; j < mat[0].length; j++){
              res.push({i:i, j:j, val:mat[i][j]});
          }
      }
      return res;
  };

  var corr_data = indexify(corr);
  var order_col = d3.range(label_col.length + 1);
  var order_row = d3.range(label_row.length + 1);

  var color = d3.scale.linear()
      .domain([-1,0,1])
      .range(['red','white','green']);

  
 
  var scale = d3.scale.linear()
      .domain([0, d3.min([50, d3.max([label_col.length, label_row.length, 4])])])
     .range([0, parseFloat(d3.select("input#zoom")[0][0].value) * 600]);

  d3.select("input#zoom").on("change", function() {
    scale = d3.scale.linear()
      .domain([0, d3.min([50, d3.max([label_col.length, label_row.length, 4])])])
            .range([0, parseFloat(this.value) * 600]);

    tick_col.transition()
        .duration(transition_time)
          .attr('font-size', scale(0.8))
          .attr('transform', function(d, i){return 'rotate(270 ' + scale(order_col[i] + 0.7) + ',0)';})
          .attr('x', function(d, i){return scale(order_col[i] + 0.7);});

    tick_row.transition()
        .duration(transition_time)
          .attr('font-size', scale(0.8))
          .attr('y', function(d, i){return scale(order_row[i] + 0.7);});

    pixel.transition()
        .duration(transition_time)
          .attr('width', scale(0.9))
          .attr('height', scale(0.9))
          .attr('y', function(d){return scale(order_row[d.i]);})
          .attr('x', function(d){return scale(order_col[d.j]);});



  });

  
 
  var label_space = 125;
  // I will make it also a function of scale and max label length

  var matrix = svg.append('g')
      .attr('class','matrix')
      .attr('transform', 'translate(' + (label_space + 10) + ',' + (label_space + 10) + ')');

  var pixel = matrix.selectAll('rect.pixel').data(corr_data);

  // as of now, data not changable, only sortable
  pixel.enter()
      .append('rect')
          .attr('class', 'pixel')
          .attr('width', scale(0.9))
          .attr('height', scale(0.9))
          .style('fill',function(d){ return color(d.val);})
          .on('mouseover', function(d){pixel_mouseover(d);})
          .on('mouseout', function(d){mouseout(d);});
          // .on('click', function(d){reorder_matrix(d.i, 'col'); reorder_matrix(d.j, 'row');});
          //the last thing works only for symmetric matrices, but with asymmetric sorting

  tick_col = svg.append('g')
      .attr('class','ticks')
      .attr('transform', 'translate(' + (label_space + 10) + ',' + (label_space) + ')')
      .selectAll('text.tick')
      .data(label_col);

  tick_col.enter()
      .append('text')
          .attr('class','tick')
          .style('text-anchor', 'start')
          .attr('transform', function(d, i){return 'rotate(270 ' + scale(order_col[i] + 0.7) + ',0)';})
          .attr('font-size', scale(0.8))
          .text(function(d){ return d; })
          .on('mouseover', function(d, i){tick_mouseover(d, i, col[i], label_row);})
          .on('mouseout', function(d){mouseout(d);})
          .on('click', function(d, i){reorder_matrix(i, 'col');});

  tick_row = svg.append('g')
      .attr('class','ticks')
      .attr('transform', 'translate(' + (label_space) + ',' + (label_space + 10) + ')')
      .selectAll('text.tick')
      .data(label_row);

  tick_row.enter()
      .append('text')
          .attr('class','tick')
          .style('text-anchor', 'end')
          .attr('font-size', scale(0.8))
          .text(function(d){ return d; })
          .on('mouseover', function(d, i){tick_mouseover(d, i, row[i], label_col);})
          .on('mouseout', function(d){mouseout(d);})
          .on('click', function(d, i){reorder_matrix(i, 'row');});

  var pixel_mouseover = function(d){
    tooltip.style("opacity", 0.8)
      .style("left", (d3.event.pageX + 15) + "px")
      .style("top", (d3.event.pageY + 8) + "px")
      .html(d.i + ": " + label_row[d.i] + "<br>" + d.j + ": " + label_col[d.j] + "<br>" + "Value: " + (d.val > 0 ? "+" : "&nbsp;") + d.val.toFixed(3));
  };

  var mouseout = function(d){
    tooltip.style("opacity", 1e-6);
  };

  var tick_mouseover = function(d, i, vec, label){
    // below can be optimezed a lot
    var indices = d3.range(vec.length);
    // also value/abs val?
    indices.sort(function(a, b){ return Math.abs(vec[b]) - Math.abs(vec[a]); });
    res_list = [];
    for(var j = 0; j < Math.min(vec.length, 10); j++) {
      res_list.push((vec[indices[j]] > 0 ? "+" : "&nbsp;") + vec[indices[j]].toFixed(3) + "&nbsp;&nbsp;&nbsp;" + label[indices[j]]);
    }
    tooltip.style("opacity", 0.8)
      .style("left", (d3.event.pageX + 15) + "px")
      .style("top", (d3.event.pageY + 8) + "px")
      .html("" + i + ": " + d + "<br><br>" + res_list.join("<br>"));
  };


  var refresh_order = function(){
      tick_col.transition()
          .duration(transition_time)
              .attr('transform', function(d, i){return 'rotate(270 ' + scale(order_col[i] + 0.7) + ',0)';})
              .attr('x', function(d, i){return scale(order_col[i] + 0.7);});

      tick_row.transition()
          .duration(transition_time)
              .attr('y', function(d, i){return scale(order_row[i] + 0.7);});

      pixel.transition()
          .duration(transition_time)
              .attr('y', function(d){return scale(order_row[d.i]);})
              .attr('x', function(d){return scale(order_col[d.j]);});
  };

  refresh_order();

  var last_k = 0;
  var last_what = 'col';
  var reorder_matrix = function(k, what){
      last_k = k;
      last_what = what;
      var order = [];
      var vec = [];
      var labels = [];
      var vecs = [];
      if(what === 'row'){  //yes, we are sorting counterpart
          vec = row[k];
          vecs = row;
          labels = label_col;  //test is if it ok
      } else if ( what === 'col' ) {
          vec = col[k];
          vecs = col;
          labels = label_row;
      }
      var indices = d3.range(vec.length);
          indices = indices.sort(function(a,b){return vec[b] - vec[a];});
      if(what === 'row' ){
          order_col = reverse_permutation(indices);
      } //not else if!
      if ( what === 'col' ) {
          order_row = reverse_permutation(indices);
      }
      refresh_order();
  };

  var reverse_permutation = function(vec){
      var res = [];
      for(var i = 0; i < vec.length; i++){
          res[vec[i]] = i;
      }
      return res;
  };
  

};
  
});