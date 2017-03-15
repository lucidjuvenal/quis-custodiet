function gra(x, y, TITULO, Subtitulo) {
    var options = {

        /*  colors: ['#5DA5A2', '#ABBC85', '#DFD3B6', '#5F5448', '#24CBE5', '#64E572', 
              '#FF9655', '#FFF263', '#6AF9C4'],*/
        credits: {
            enabled: false
        },
        chart: {
            renderTo: 'id_Grafico_tabla',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 5,
                beta: 0,
                depth: 75,
                viewDistance: 100
            },
            events: {
                load: function (event) {
                    var cats = this.xAxis[0].categories;
                    var theData = this.series[0].data;
                    var newCats = [];

                    for (var i = 0; i < cats.length; i++) {
                        newCats.push(cats[i] + '<br/>' + theData[i].y)
                    }

                    this.xAxis[0].setCategories(newCats);
                }
            }

        },
        title: {
            text: TITULO,

            style: {
                color: '#0E3F68',
                fontSize: '15px'

            }
        },
        subtitle: {
            text: Subtitulo,
        },
        xAxis: {
            //type: 'category',     
            categories: x,
            labels: {
                style: {
                    align: 'center',
                    color: '#0E3F68'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '# de Votos'
            }
        },
        /*tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>$ {point.y:.0f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },*/
        tooltip: {
            // valuePrefix: '$ '   
            pointFormat: '',
            shared: false


        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0

            }
            ,
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    align: 'center',
                    color: '#0E3F68',
                    // x: -10, es para insertar detro de la barra en horizontal BAR
                    //  format: '{point.y}'
                    formatter: function () {
                        var mychart = $('#id_Grafico_tabla').highcharts();
                        var mytotal = 0;

                        for (i = 0; i < mychart.series.length; i++) {
                            for (j = 0; j < mychart.series[i].data.length; j++) {
                                if (mychart.series[i].visible) {
                                    mytotal += parseInt(mychart.series[i].yData[j]);
                                }
                            }
                        }
                        var pcnt = (this.y / mytotal) * 100;
                        return Highcharts.numberFormat(pcnt) + '%';
                    }
                }
            },
            column: {
                depth: 100
            }
        },
        dataLabels: {
            inside: true,
            enabled: true,
            useHTML: true,
            formatter: function () {
                if (new Date().setHours(0, 0, 0, 0) !== new Date(this.y).setHours(0, 0, 0, 0)) {
                    if (this.y == this.point.high) {
                        return '<span style="color:black">' + Highcharts.dateFormat('%Y', this.y) + ' - ' + this.point.name + '</span>';
                    }
                    return '<span style="color:black">' + Highcharts.dateFormat('%Y', this.y) + '</span>';
                }
                else return '';
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: true
        },
        series:
          y
    }
    var chart = new Highcharts.Chart(options);
    chart.redraw();
}

function graDrill(x, y, TITULO, Subtitulo, drill, htmlImg, arrColores) {
    var h = 0;
    var options = {

        colors: arrColores,
       
        credits: {
            enabled: false
        },
        chart: {
            renderTo: 'id_Grafico_tabla',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 5,
                beta: 0,
                depth: 75,
                viewDistance: 100
            },
            events: {
                load: function (event) {
                    var cats = this.xAxis[0].categories;
                    var theData = this.series[0].data;
                    var newCats = [];

                    for (var i = 0; i < cats.length; i++) {
                        newCats.push(cats[i] + '<br/> ' + theData[i].y)
                    }

                    this.xAxis[0].setCategories(newCats);
                },
                drilldown: function (e) {
                    h = 24;
                        var chart = this;
                        chart.setTitle(null, {
                            text: e.seriesOptions.id
                        });
                    },
                drillup: function() {
                        var chart = this;
                        chart.setTitle(null, {
                            text: Subtitulo
                    });
                }
            },
            animation: {
                duration: 2700
            }

        },
        title: {
            text: TITULO,

            style: {
                color: '#0E3F68',
                fontSize: '15px'

            }
        },
        subtitle: {
            text: Subtitulo,
        },
        xAxis: {
            type: 'category',
            // categories: x,
            labels: {
                style: {
                    align: 'center',
                    color: '#0E3F68',
                    fontWeight: 'normal'
                }/*,
                x: 5,
                useHTML: true,
                formatter: function () {
                    return '<img src="http://highcharts.com/demo/gfx/sun.png"><img>&nbsp;';
                }*/
            }
        },
        yAxis: {
            min: 0,

            title: {
                text: '# de Votos'
            }
        },
        /*tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>$ {point.y:.0f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },*/
        tooltip: {
            // valuePrefix: '$ '   
            pointFormat: '',
            shared: false,
            enabled: false,


        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0

            }
            ,
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    align: 'center',
                    color: '#0E3F68',
                    useHTML: htmlImg,
                    // x: -10, es para insertar detro de la barra en horizontal BAR
                    //  format: '{point.y}'
                    formatter: function () {
                        h++;
                        var mychart = $('#id_Grafico_tabla').highcharts();
                        var mytotal = 0;

                        for (i = 0; i < mychart.series.length; i++) {
                            for (j = 0; j < mychart.series[i].data.length; j++) {
                                if (mychart.series[i].visible) {
                                    mytotal += parseInt(mychart.series[i].yData[j]);
                                }
                            }
                        }
                        var pcnt = (this.y / mytotal) * 100;
                             if (TITULO.includes("PRESIDENT"))
                                return '<img src="imagenes/Candidato/can_' + (h - 25) + '.png" width="64px"><img><br><center><span style="color:#000;">' + Highcharts.numberFormat(pcnt) + '%</center></span>';
                            else
                                 return Highcharts.numberFormat(pcnt) + '%';
                    }
                }
            },
            column: {
                depth: 100
            }
        },
        dataLabels: {
            inside: true,
            enabled: true,
            useHTML: true,
            formatter: function () {
                if (new Date().setHours(0, 0, 0, 0) !== new Date(this.y).setHours(0, 0, 0, 0)) {
                    if (this.y == this.point.high) {
                        return '<span style="color:black">' + Highcharts.dateFormat('%Y', this.y) + ' - ' + this.point.name + '</span>';
                    }
                    return '<span style="color:black">' + Highcharts.dateFormat('%Y', this.y) + '</span>';
                }
                else return '';
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: true
        },
        series:
          y,
        drilldown: {
            drillUpButton: {
                relativeTo: 'spacingBox',
                position: {
                    y: -4,
                    x: -50
                },
                theme: {
                    fill: 'white',
                    'stroke-width': 1,
                    stroke: 'silver',
                    r: 5
                }
            },
            activeAxisLabelStyle: {
                textDecoration: 'none',
                fontWeight: 'normal'
            },
            activeDataLabelStyle: {
                textDecoration: 'none',
                fontWeight: 'bold'
            },
            series: drill

        }
    }
    var chart = new Highcharts.Chart(options);
    chart.redraw();

    graDrillPie(x, y, TITULO, Subtitulo, drill, arrColores);
}

function graDrillPie(x, y, TITULO, Subtitulo, drill, arrColores) {
    var options = {

        colors: arrColores,

        credits: {
            enabled: false
        },
        chart: {
            renderTo: 'id_Grafico_Pie',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            type: 'pie',
            events: {
                load: function (event) {
                    var cats = this.xAxis[0].categories;
                    var theData = this.series[0].data;
                    var newCats = [];

                    for (var i = 0; i < cats.length; i++) {
                        newCats.push(cats[i] + '<br/> ' + theData[i].y)
                    }

                    this.xAxis[0].setCategories(newCats);
                },
                drilldown: function (e) {
                    h = 24;
                    var chart = this;
                    chart.setTitle(null, {
                        text: e.seriesOptions.id
                    });
                },
                drillup: function () {
                    var chart = this;
                    chart.setTitle(null, {
                        text: Subtitulo
                    });
                }
            }

        },
        title: {
            text: TITULO,

            style: {
                color: '#0E3F68',
                fontSize: '15px',

            }
        },
        subtitle: {
            text: Subtitulo,
        },
        xAxis: {
            type: 'category',
            categories: x,
            labels: {
                style: {
                    align: 'center',
                    color: '#0E3F68',
                    fontWeight: 'normal'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '# de Votos'
            }
        },
        /*tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>$ {point.y:.0f} </b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },*/
        tooltip: {
            // valuePrefix: '$ '   
            pointFormat: '',
            shared: false


        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0

            }
            ,
            series: {
                borderWidth: 0,
                style: {
                    color: '#FF0000',
                    fontSize: '15px',

                },
                dataLabels: {
                    enabled: true,
                    align: 'center',
                    fontWeight: 'normal',
                    //   color: '#0E3F68',
                    // x: -10, es para insertar detro de la barra en horizontal BAR
                    //  format: '{point.y}'
                    formatter: function () {
                        var mychart = $('#id_Grafico_Pie').highcharts();
                        var mytotal = 0;

                        for (i = 0; i < mychart.series.length; i++) {
                            for (j = 0; j < mychart.series[i].data.length; j++) {
                                if (mychart.series[i].visible) {
                                    mytotal += parseInt(mychart.series[i].yData[j]);
                                }
                            }
                        }
                        var pcnt = (this.y / mytotal) * 100;
                        return '<span style="font-weight: normal; color:black">' + this.point.name + ':  <b>' + Highcharts.numberFormat(pcnt) + '% </b></span>';
                    }
                }
            },
            column: {
                depth: 100
            },
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: false
            }
        },
        dataLabels: {
            inside: true,
            enabled: true,
            useHTML: true,
            formatter: function () {
                if (new Date().setHours(0, 0, 0, 0) !== new Date(this.y).setHours(0, 0, 0, 0)) {
                    if (this.y == this.point.high) {
                        return '<span style="color:black">' + Highcharts.dateFormat('%Y', this.y) + ' - ' + this.point.name + '</span>';
                    }
                    return '<span style="color:black">' + Highcharts.dateFormat('%Y', this.y) + '</span>';
                }
                else return '';
            }
        },
        legend: {
            enabled: true
        },
        exporting: {
            enabled: true
        },
        series:
          y,
        drilldown: {
            activeAxisLabelStyle: {
                textDecoration: 'none',
                fontWeight: 'normal'
            },
            activeDataLabelStyle: {
                textDecoration: 'none',
                fontWeight: 'normal'
            },
            series: drill
        }
    }
    var chart = new Highcharts.Chart(options);
    chart.redraw();
}