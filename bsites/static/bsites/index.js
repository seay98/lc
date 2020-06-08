$(document).ready(function () {
    $("#markbtn").click(function () {
        $.ajax({
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            url: "ci",
            success: function (result) {
                //console.log(result.slice(0, -3) + ']');
                data = result.slice(0, -3) + ']'
                locations = jQuery.parseJSON(data);
                loadpoints(locations);
            },
            error: function (e) {
                console.log(e.status);
                console.log(e.responseText);
            }
        });
    });
    $("#cilocbtn").click(function () {
        $.ajax({
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            url: "ciloc",
            success: function (result) {
                //console.log(result.slice(0, -3) + ']');
                data = result.slice(0, -3) + ']'
                locations = jQuery.parseJSON(data);
                loadpoints(locations);
                // alert(locations[0].coverage);
                addPolygon(locations[0].coverage, '#ccebc5');
                addPolygon(locations[0].signalrange, '#ffe4e1');
                // addPolygon([
                //     new AMap.LngLat(102.712654,25.060810),
                //     new AMap.LngLat(102.712104,25.057098),
                //     new AMap.LngLat(102.712992,25.057078),
                //     new AMap.LngLat(102.713863,25.057233),
                //     new AMap.LngLat(102.714678,25.057553),
                //     new AMap.LngLat(102.715399,25.058025)
                // ]);
            },
            error: function (e) {
                console.log(e.status);
                console.log(e.responseText);
            }
        });
    });
});
var map = new AMap.Map('container', {
    zoom: 13
});

function loadpoints(locations) {
    var icon = new AMap.Icon({
        size: new AMap.Size(12, 12),    // 图标尺寸
        image: 'https://a.amap.com/jsapi_demos/static/demo-center/marker/marker.png',  // Icon的图像
        imageOffset: new AMap.Pixel(0, 0),  // 图像相对展示区域的偏移量，适于雪碧图等
        imageSize: new AMap.Size(12, 12)   // 根据所设置的大小拉伸或压缩图片
    });

    var locs = [];
    var label = [];
    for (var i in locations) {//遍历packJson 对象的每个key/value对,k为key
        locs[i] = new AMap.LngLat(parseFloat(locations[i].lon), parseFloat(locations[i].lat));
        label[i] = locations[i].title;
    }
    //var gps = [locations.lat, locations.lon];
    var marker = [];
    var labelOffset = new AMap.Pixel(0, -5);
    var pos;
    map.setCenter(locs[0]);
    for (var i = 0; i < locs.length; i++) {
        if (pos == locs[i]) continue;
        pos = locs[i];
        marker[i] = new AMap.Marker({
            position: locs[i],   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
            offset: new AMap.Pixel(-6, -6),
            icon: icon,
            title: 'lac',
            zoom: 13,
            label: {
                direction: 'top',
                content: "<div class='labelContent'>" + label[i] + "</div>",
                offset: labelOffset,
            }
        });
        map.add(marker[i]);
    }
    AMap.convertFrom(locs, 'gps', function (status, result) {
        if (result.info === 'ok') {
            var lnglats = result.locations;
            // alert(lnglats);

            // var labelOffset = new AMap.Pixel(0, -5);
            // for (var i = 0; i < lnglats.length; i++) {
            //     marker[i] = new AMap.Marker({
            //         position: lnglats[i],   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
            //         offset: new AMap.Pixel(0, 0),
            //         icon: icon,
            //         title: 'lac',
            //         zoom: 13,
            //         label: {
            //             direction: 'top',
            //             content: "<div class='labelContent'>"+label[i]+"</div>",
            //             offset: labelOffset,
            //         }
            //     });
            //     map.add(marker[i]);
            // }
        }
    });
};

function addPolygon(data, color) {
    let point = data.split(',');
    let points = [];
    let j = 0;
    for (var i = 0; i < point.length; i=i+2) {
        points[j++] = new AMap.LngLat(parseFloat(point[i]), parseFloat(point[i+1]));
    }
    // alert(points);
    let polygon = new AMap.Polygon({
      path: points,
      fillColor: color,
      strokeOpacity: 1,
      fillOpacity: 0.5,
      strokeColor: '#2b8cbe',
      strokeWeight: 1,
      strokeStyle: 'dashed',
      strokeDasharray: [5, 5],
    });
    polygon.on('mouseover', () => {
      polygon.setOptions({
        fillOpacity: 0.7,
        fillColor: '#7bccc4'
      })
    });
    polygon.on('mouseout', () => {
      polygon.setOptions({
        fillOpacity: 0.5,
        fillColor: color

      })
    });
    map.add(polygon);
  };
