var text = '';
var lactext = '';
$(document).ready(function () {

    // 给按钮绑定事件
    document.getElementById("cisbtn").onclick = clickOn;
    // document.getElementById("clickOff").onclick = clickOff;

    $("#markbtn").click(function () {
        $.ajax({
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            url: "ci",
            success: function (result) {
                //console.log(result.slice(0, -3) + ']');
                locations = jQuery.parseJSON(result);
                masspoints(locations);
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
                locations = jQuery.parseJSON(result);
                // loadpoints(locations);
                for (var i in locations) {
                    addPolygon(locations[i].coverage, '#ffe4e1');
                }
            },
            error: function (e) {
                console.log(e.status);
                console.log(e.responseText);
            }
        });
    });
    $("#clnbtn").click(function () {
        for(var i in polygons){
            map.remove(polygons[i].pg);
            var chk = document.getElementById(polygons[i].id);
            if (chk) chk.checked = false;
        }
        polygons.splice(0,polygons.length);
    });
    $("#srchbtn").click(function () {
        var lac = document.getElementById("lacnum").value;
        var ci = document.getElementById("cinum").value;
        $.ajax({
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            url: "cild",
            data:{
                lac: lac,
                ci: ci
            },
            success: function (result) {
                var cil = jQuery.parseJSON(result);
                if (cil.id==''){
                    log.success("未找到相关信息");
                    return;
                }
                var cic = '<span><font>基站:' + cil.lac + '-' + cil.ci1 + ';运营商:' + sp[parseInt(cil.mnc)] +'</font></span></p>';
                // var url = '<a href="'+cis[i].id+'">查看</a></p>';
                var url = '<p><input id="'+cil.id+'" type="checkbox" onclick="showrange(this)"  style="height:12px"></input>';
                
                text = text + url + cic;
                // alert(text);
                document.querySelector("#text").innerHTML = text;
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

// JSAPI 2.0 支持显示设置 zIndex, zIndex 越大约靠前，默认按顺序排列
var style = [{
    url: 'https://webapi.amap.com/images/mass/mass0.png',
    anchor: new AMap.Pixel(6, 6),
    size: new AMap.Size(11, 11),
    zIndex: 3,
}, {
    url: 'https://webapi.amap.com/images/mass/mass1.png',
    anchor: new AMap.Pixel(4, 4),
    size: new AMap.Size(7, 7),
    zIndex: 2,
}, {
    url: 'https://webapi.amap.com/images/mass/mass2.png',
    anchor: new AMap.Pixel(3, 3),
    size: new AMap.Size(5, 5),
    zIndex: 1,
}
];

function setStyle(multiIcon) {
    if (multiIcon) {
        mass.setStyle(style);
    } else {
        mass.setStyle(style[2]);
    }
};

function masspoints(locations) {
    var data = [];
    var pd = {};
    for (var i in locations) {
        pd = {lnglat: [locations[i].lon, locations[i].lat], name: locations[i].title, style:1};
        data.push(pd);
    }

    var mass = new AMap.MassMarks(data, {
        opacity: 0.8,
        zIndex: 111,
        cursor: 'pointer',
        style: style
    });

    var marker = new AMap.Marker({content: ' ', map: map});

    mass.on('mouseover', function (e) {

        marker.setPosition(e.data.lnglat);
        marker.setLabel({content: e.data.name})
    });

    mass.setMap(map);
    // alert(locations[0].lon);
    map.setCenter(new AMap.LngLat(parseFloat(locations[0].lon), parseFloat(locations[0].lat)));
};

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
    for (var i = 0; i < point.length; i = i + 2) {
        points[j++] = new AMap.LngLat(parseFloat(point[i]), parseFloat(point[i + 1]));
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
    return polygon;
};

sp = ['移动','联通',,,,,,,,,,'电信'];
polygons = [];
lacpg = [];
function showInfoClick(e){
    //alert("click");
    var marker = new AMap.Marker({
        map: map,
        draggable:true,
        position: [e.lnglat.getLng(), e.lnglat.getLat()]
    });
    // ci
    text = ''
    $.ajax({
        type: "GET",
        contentType: "application/json;charset=UTF-8",
        url: "cis",
        data:{
            lat: e.lnglat.getLat(),
            lon: e.lnglat.getLng()
        },
        success: function (result) {
            cis = jQuery.parseJSON(result);
            for (var i in cis) {
                var rsc = parseInt(cis[i].rs);
                var color = "gray";
                if (rsc > -65) {
                    color = "green";
                } else if (rsc<-100) {
                    color = "red";
                }
                var cic = '<span><font color="'+color+'">基站:' + cis[i].lac + '-' + cis[i].ci1 + ';运营商:' + sp[parseInt(cis[i].mnc)] + ';增益:'+cis[i].rs+'</font></span></p>';
                var url = '<p><input id="'+cis[i].id+'" type="checkbox" onclick="showrange(this)"  style="height:12px"></input>';
                
                text = text + url + cic;
            }
            // alert(text);
            document.querySelector("#text").innerHTML = text;
        },
        error: function (e) {
            console.log(e.status);
            console.log(e.responseText);
        }
    });
    document.querySelector("#text").innerText = text;

    // lac
    lactext = ''
    $.ajax({
        type: "GET",
        contentType: "application/json;charset=UTF-8",
        url: "lacs",
        data:{
            lat: e.lnglat.getLat(),
            lon: e.lnglat.getLng()
        },
        success: function (result) {
            lacs = jQuery.parseJSON(result);
            for (var i in lacs) {
                var color = "gray";
                var lacc = '<span><font color="'+color+'">基站:' + lacs[i].lac + ';运营商:' + sp[parseInt(lacs[i].mnc)] +'</font></span></p>';
                var url = '<p><input id="'+lacs[i].id+'" type="checkbox" onclick="showlacrange(this)"  style="height:12px"></input>';
                
                lactext = lactext + url + lacc;
            }
            // alert(text);
            document.querySelector("#lactext").innerHTML = lactext;
        },
        error: function (e) {
            console.log(e.status);
            console.log(e.responseText);
        }
    });
    document.querySelector("#lactext").innerText = lactext;
};
function showrange(chk){
    if (chk.checked==true) {
        $.ajax({
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            url: "cil/"+chk.id,
            success: function (result) {
                locations = jQuery.parseJSON(result);
                // loadpoints(locations);
                pg = addPolygon(locations[0].signalrange, '#ffe4e1');
                pgobj = {id:chk.id, pg:pg};
                polygons.push(pgobj);
            },
            error: function (e) {
                console.log(e.status);
                console.log(e.responseText);
            }
        });
    } else {
        for (var i in polygons){
            if (polygons[i].id==chk.id) {
                map.remove(polygons[i].pg);
                polygons.splice(i, 1);
                break;
            }
        }
    }  
};
function showlacrange(chk){
    if (chk.checked==true) {
        $.ajax({
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            url: "lacr/"+chk.id,
            success: function (result) {
                locations = jQuery.parseJSON(result);
                pg = addPolygon(locations[0].coverage, '#ffe4e1');
                pgobj = {id:chk.id, pg:pg};
                lacpg.push(pgobj);
            },
            error: function (e) {
                console.log(e.status);
                console.log(e.responseText);
            }
        });
    } else {
        for (var i in lacpg){
            if (lacpg[i].id==chk.id) {
                map.remove(lacpg[i].pg);
                lacpg.splice(i, 1);
                break;
            }
        }
    }  
};
function showInfoDbClick(e){
    // var text = '您在 [ '+e.lnglat.getLng()+','+e.lnglat.getLat()+' ] 的位置双击了地图！'
    // document.querySelector("#text").innerText = text;
};
function showInfoMove(){
    // var text = '您移动了您的鼠标！'
    // document.querySelector("#text").innerText = text;
};
// 事件绑定
function clickOn(){
    // log.success("绑定事件!");  
    map.on('click', showInfoClick);
    map.on('dblclick', showInfoDbClick);
    map.on('mousemove', showInfoMove);
};
// 解绑事件
function clickOff(){
    // log.success("解除事件绑定!"); 
    map.off('click', showInfoClick);
    map.off('dblclick', showInfoDbClick);
    map.off('mousemove', showInfoMove);
};

