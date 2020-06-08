var img1_buttonFlag = 0; // 是否想要重新上传

// 图片1上传，img1-button的点击事件
function img1_upload() {
    var input = document.getElementById("img1-input");
    if (typeof (FileReader) === 'undefined') {
        // result.innerHTML = "抱歉，你的浏览器不支持 FileReader，请使用现代浏览器操作！";
        alert("抱歉，你的浏览器不支持 FileReader，请使用现代浏览器操作！")
        input.setAttribute('disabled', 'disabled');
    } else {
        input.addEventListener('change', readFile, false);
    }
    $(input).click();
}

// 将生成的图片转为base64，自动调用
function readFile() {
    var file = document.getElementById("img1-input").files[0];  // 文件对象
    if (file === undefined) {  // 检测上传的图片是否为空
        return false;
    } else {
        console.log('change');
        if (img1_buttonFlag === 0) {
            img1_buttonFlag = 1;
        } else {
            jcropApi && jcropApi.destroy();
            jcropApi = undefined;
            $.Jcrop.component.DragState.prototype.touch = null;
            $('#img2-button').text('提取人像').attr({
                'disabled': 'disabled',
                'onclick': 'getbody()',
            });
            $('#img3-button').attr('disabled', 'disabled');
        }

        $('#img1-button').text('重新上传')
        if (!/image\/\w+/.test(file.type)) {  // 检测上传的是否为图片
            alert("请确保文件为图像类型");
            return false;
        } else if (file.size > 1024 * 1024 * 1.9) {
            alert("图片大小不得大于1.9MB，请您重新上传");
            return false;
        } else {  // 格式正确
            var reader = new FileReader();  // 创建一个文件对象
            reader.readAsDataURL(file);  // 读取url
            // console.log(this.result);
            reader.onload = function (e) {  // 加载文件，展示图片
                // result.innerHTML = '<img src="' + this.result + '" alt=""/>';
                $('#img1').attr('src', this.result);
                $('#img2-button').removeAttr('disabled');
            }
        }
    }

}

// 提取人像，img2-button的第一个点击事件
function getbody(url) {
    $('.waiting', parent.document).html('正在提取人像<br>这需要一段时间').show();
    $('#img2-button').attr('disabled', 'disabled')
    var image = $('#img1').attr('src').split('base64,')[1];
    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: '/APPApi/graduationPhoto/getbody/',
        data: {
            image: encodeURI(image),
        },
        success: function (response) {
            if (response.foreground) {
                $('#img2').attr('src', 'data:image/jpg/png;base64,' + response.foreground);
                $('#img2-button').text('截取头像').removeAttr('disabled').attr('onclick', 'cut_head()');
                create_jcrop(); // 启动jcrop，进行图像截取

            } else if (response.error_code == "18") {
                // 高并发处理
                alert('抱歉，当前服务器繁忙，请您稍等几秒后重新提交');
                // 设定button等待几秒重新提交
                var button_clock = 5;
                var timing = setInterval(function () {
                    if (button_clock > 0) {
                        $('#img2-button').text(button_clock);
                    } else {
                        $('#img2-button').text('提取人像').removeAttr('disabled');
                        clearInterval(timing);
                    }
                    button_clock--;
                }, 1000)
            } else {
                alert('抱歉，提取人像失败，请您尝试重新提取');
            }
            $('.waiting', parent.document).hide();
        },
        error: function (e) {
            console.log(e);
            alert('抱歉，提取人像失败，请您尝试重新提取');
            $('.waiting', parent.document).hide();
        }
    })
}

// 截图，自动调用
var jcropApi

function create_jcrop() {
    $('#img2').Jcrop({
        allowSelect: false, // 不允许新选框
        trackDocument: false, // 不允许在图片外选择
        bgColor: "lightgray", // 背景设置为灰色
        aspectRatio: 1,  // 选框宽高比为1，即为正方形
        boxWidth: document.querySelector("#img1").width,  // 画布宽度
        boxHeight: document.querySelector("#img1").height,  // 画布高度
        setSelect: [30, 60, 130, 160], // 创建选框，参数格式为：[x, y, x2, y2]
        touchSupport: "touchmove",
        onSelect: get_jcrop_coords,
    }, function () {
        jcropApi = this;
    });
    coord = [30, 60, 160, 190, 130, 130];  // 初始化全局截图信息
}

// jcrop的回调函数
function get_jcrop_coords(coords) {
    var x1 = coords.x;
    var y1 = coords.y;
    var x2 = coords.x2;
    var y2 = coords.y2;
    var w = coords.w;
    var h = coords.h;
    coord = [x1, y1, x2, y2, w, h];
}

// 确认截图信息，将头像和身体拼接，img2-button的第二个点击事件
function cut_head() {
    var img2 = document.getElementById("img2");
    var cavs = document.getElementById("img3-canvas");
    var ctx = cavs.getContext('2d');
    ctx.clearRect(0, 0, cavs.width, cavs.height);  // 清屏
    var pic_url = $("#my-photo").attr('pic-url');

    // 使用blob解决跨域问题
    const xhr = new XMLHttpRequest();
    xhr.open('GET', pic_url, true);
    xhr.responseType = 'blob';
    xhr.onload = function () {
        if (parseInt(this.status, 10) === 200) {
            var img3_back = new Image(); //定义一个图片对象
            img3_back.src = URL.createObjectURL(this.response);
            img3_back.onload = function () { //此处必须注意！后面所有操作均需在图片加载成功后执
                // todo: 图片请求成功之后的操作
                ctx.drawImage(img2, coord[0], coord[1], coord[4], coord[5], 78, 10, 40, 40); // 绘制头像
                ctx.drawImage(img3_back, 0, 0, cavs.width, cavs.height); // 绘制背景

                var url = cavs.toDataURL("image/png");
                $('#img3').attr('src', url);
                $('#img3-button').removeAttr('disabled');
            }
        }
    };
    xhr.send();
}

// 提交制作好的毕业照片，img3-button的点击事件
function img3_upload() {
    $("#img3-button").attr('disabled', 'disabled');  // 按钮禁用
    var img3 = $("#img3"); // 图片3的base64编码信息
    $.ajax({
        type: 'POST',
        url: '/APPApi/graduationPhoto/get_photo/',
        data: {
            img3: img3.attr('src')
        },
        success: function () {
            location.reload(); // 刷新当前页面，让其重新加载
        }
    })
}

// 重新制作图片，img4-button的点击事件
function img4_remake() {
    $("#img4-button").attr('disabled', 'disabled');  // 按钮禁用
    $("#my-photo").html('<div class="image-box">\n' +
        '        <div class="image-contain">\n' +
        '            <img id="img1" src="https://iph.href.lu/200x240?text=我的照片&fg=666666&bg=cccccc" title="等待您上传一张图"\n' +
        '                 alt="等待您上传一张图">\n' +
        '        </div>\n' +
        '\n' +
        '        <input id="img1-input" name="img1-input" style="display: none" type="file"\n' +
        '               accept="image/png,image/jpg,image/jpeg">\n' +
        '        <button id="img1-button" onclick="img1_upload()">上传</button>\n' +
        '    </div>\n' +
        '    <div class="image-box">\n' +
        '        <div class="image-contain">\n' +
        '            <img id="img2" src="https://iph.href.lu/200x240?text=人像抠图&fg=666666&bg=cccccc" title="等待您上传一张图"\n' +
        '                 alt="等待您上传一张图">\n' +
        '        </div>\n' +
        '        <button id="img2-button" disabled="disabled" onclick="getbody()">提取人像</button>\n' +
        '    </div>\n' +
        '    <div class="image-box">\n' +
        '        <div class="image-contain">\n' +
        '            <img id="img3" src="https://iph.href.lu/200x240?text=合成照片&fg=666666&bg=cccccc" title="等待您上传一张图"\n' +
        '                 alt="等待您上传一张图">\n' +
        '        </div>\n' +
        '        <button id="img3-button" disabled="disabled" onclick="img3_upload()">提交</button>\n' +
        '    </div>');
    parent.reinitIframe(); // 重置本页面的高度
}

// 展示大合影
function showPhotos(photos_list) {
    // todo: 基本的思路是，首先算出来每一排的人数，然后从最后一排开始排序
    var canvas = document.getElementById("graduation-canvas");
    var ctx = canvas.getContext('2d');
    var width = canvas.width; // 画布宽度
    var height = canvas.height; // 画布高度
    var student_width = 40; // 每个学生人像的宽度
    var pai = Math.ceil(photos_list.length / 5); // 一共有几排
    var y_axis_first = 350; // 第一排同学的纵坐标
    var x_axis = 0; // 每个人的横坐标
    var y_axis = 0; // 每个人的纵坐标

    // 使用blob解决跨域问题
    const xhr = new XMLHttpRequest();
    xhr.open('GET', "https://cdn.img.wenhairu.com/images/2020/06/04/Yh0yA.jpg", true);
    xhr.responseType = 'blob';
    xhr.onload = function () {
        if (parseInt(this.status, 10) === 200) {
            var graduation_bk = new Image(); //定义一个图片对象
            graduation_bk.src = URL.createObjectURL(this.response);
            graduation_bk.onload = function () { //此处必须注意！后面所有操作均需在图片加载成功后执
                // todo: 图片请求成功之后的操作
                ctx.drawImage(graduation_bk, 0, 0, width, height); // 绘制背景
                // 首先需要对排进行循环
                var student_index = 0;
                for (var pai_index = 0; pai_index < pai; pai_index++) {
                    var student_num = pai_index + 1 > (pai - photos_list.length % pai) ? Math.floor(photos_list.length / pai) + 1 : Math.floor(photos_list.length / pai); // 这一排的学生人数
                    x_axis = (width - student_num * student_width) / 2; // 第一个人的横坐标
                    if (x_axis_last && x_axis_last === x_axis) {
                        x_axis -= student_width * 0.5;
                    }
                    var x_axis_last = x_axis;
                    y_axis = y_axis_first - pai * student_width * 0.6 + pai_index * student_width * 0.6;
                    for (var i = 0; i < student_num; i++) {
                        x_axis = x_axis_last + i * student_width;
                        (function (x_axis, y_axis, student_index) {
                            var img = new Image();
                            img.src = photos_list[student_index];
                            img.onload = function () {
                                ctx.drawImage(img, x_axis, y_axis, student_width, student_width * 1.2);
                                if (student_index + 1 === photos_list.length) {
                                    ctx.font = "300px bold 黑体";
                                    ctx.fillStyle = "rgba(255, 255, 255, 0.3)";
                                    ctx.textAlign = "center";
                                    ctx.textBaseline = "middle";
                                    ctx.fillText("电光16", width / 2, height / 2);
                                    var url = canvas.toDataURL("image/png");
                                    $('#graduation-bk').attr('src', url);
                                }
                            }
                        })(x_axis, y_axis, student_index)

                        student_index++;
                    }
                }

            }
        }
    };
    xhr.send();
}