$(document).ready(function () {
    console.log('load');
    $('#button').click(function () {
        test();
    })
    imgupload();

});

function test() {
    var canshu1 = $('#canshu1').val();
    var canshu2 = $('#canshu2').val();
    var image = $('#image-area').attr('src');
    // console.log(image)
    var postData = 'api_key=spdG7xF9371DOVDvv0-iCDw8pZAcOsKt&api_secret=6U5sm3AxgWllyV3vwH1pdY6-Duc_yHFd'
        + '&template_url=https://cdn.img.wenhairu.com/images/2020/05/29/YtJhj.jpg'
        // + '&template_rectangle=251,167,169,169'
        + '&merge_base64=' + image
        + '&merge_rate=' + canshu1
        + '&feature_rate=' + canshu2;

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface',
        data: postData,
        success: function (response) {
            if (typeof (response.error_message) == "undefined") {
                // todo: 在这里添加生成后的逻辑，response.result 为生成图的base64编码
                $('.uploadpic').attr('src', 'data:image/jpg/png;base64,' + response.result);
            } else {
                // todo: 在这里添加上传失败的逻辑
                alert('请重新上传照片');
            }
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText);
            // todo: 在这里添加上传失败的逻辑
            alert('请重新上传照片');
        }
    });
}

function imgupload() {
    var input = document.getElementById("image");
    // var result = document.getElementById("result");
    // var img_area = document.getElementById("img_area");
    if (typeof (FileReader) === 'undefined') {
        // result.innerHTML = "抱歉，你的浏览器不支持 FileReader，请使用现代浏览器操作！";
        alert("抱歉，你的浏览器不支持 FileReader，请使用现代浏览器操作！")
        input.setAttribute('disabled', 'disabled');
    } else {
        input.addEventListener('change', readFile, false);
    }
}

function readFile() {
    console.log("in")
    var file = document.getElementById("image").files[0];
    var image_area = document.getElementById("image-area")
    // console.log(fiol);
    //这里我们判断下类型如果不是图片就返回 去掉就可以上传任意文件
    if (!/image\/\w+/.test(file.type)) {
        alert("请确保文件为图像类型");
        return false;
    }
    var reader = new FileReader();
    reader.readAsDataURL(file);
    // console.log(this.result);
    reader.onload = function (e) {
        // result.innerHTML = '<img src="' + this.result + '" alt=""/>';
        image_area.innerHTML = '<div class="sitetip">图片img标签展示：</div><img src="' + this.result + '" alt=""/>';
    }
}

