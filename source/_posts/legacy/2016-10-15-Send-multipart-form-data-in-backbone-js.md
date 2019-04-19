---
title: Send multipart/form-data in backbone.js
date: 2016-10-15 12:48:54
tags: ["backbone", "multipart", "javascript"]
---
如何使用Backbone框架发送multipart/form-data格式的数据，特别是发送二进制文件。

<!-- more -->

我们知道，下面的代码会向服务器发送一个PATCH请求：
``` 
var image = 'image file';
model.save ({'image':image}, {patch:true});
```
此时的HTTP请求是这样的:
```
PATCH /profile/2/ HTTP/1.1
Host: api.lvxin14.com
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Inp5LWxpMTRAbWFpbHMudHNpbmdodWEuZWR1LmNuIiwiZXhwIjoxNDc2MzczNjc4LCJ1c2VyX2lkIjoyLCJvcmlnX2lhdCI6MTQ3NjM3MDY3OCwidXNlcm5hbWUiOiJsaXpleWFuIn0.V3AVk9etbYlWtUmN44OKwYw7jXWCehGnG3prswYxtIQ
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: 45e35729-3eed-f1ee-8ee1-47d7d764cb45

{
	"image": "image file"
}
```

这个时候在`save`的第一个参数中指定的属性会以键值对的形式发送。但是如果我们要发送一个文件呢？
文件可以用`multipart/form-data`的格式发送。
首先，要在对应的表单中设置格式：
{% raw %}
``` html
<form enctype="multipart/form-data">
</form>
```
{% endraw %}
然后，在backbone中`save`的时候要使用`FormData`，像这样：
``` javascript
var formData = new FormData;
formData.append('real_name', $('#athena-realname-input').val());
formData.append('icon_image', this.imgFile);
formData.append('school', $('#athena-school-input').val());
formData.append('department', $('#athena-department-input').val());
formData.append('genders', $('#athena-gender-input').val());
this.model.save(null, {
    data: formData,
    patch: true,
    wait: true,
    emulateJSON: true,
    contentType: false,
    processData: false
});
```
注意，上面的键值对中只有`icon_image`发送的是文件。接下里我们看一下发送的`this.imgFile`要怎么取得：
``` javascript
var PublicProfileView = Backbone.View.extend({
    el: $('#athena-profile-setting'),
    imgFile: null,
    events: {
        'submit #athena-public-profile-form': 'uploadProfile',
        "change #athena-avatar-input": 'openAvatar'
    },
    template: _.template($('#tmplt-profile-setting').html()),
    render: function () {
        this.$el.html(this.template({
            "image": this.model.get('icon_image'),
            "realname": this.model.get('real_name'),
            "school": this.model.get('school'),
            "department": this.model.get('department'),
            "gender": this.model.get('genders')
        }));
        return this;
    },
    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
    },
    openAvatar: function (event) {
        this.imgFile = event.currentTarget.files[0];
        // alert (file);
        var reader = new FileReader();
        reader.onload = function (fileEvent) {
            $('#athena-avatar-img').src = fileEvent.target.result;
        }.bind(this);
        reader.readAsDataURL(this.imgFile);
    },
    uploadProfile: function (event) {
        event.preventDefault();
        var formData = new FormData;
        formData.append('real_name', $('#athena-realname-input').val());
        formData.append('icon_image', this.imgFile);
        formData.append('school', $('#athena-school-input').val());
        formData.append('department', $('#athena-department-input').val());
        formData.append('genders', $('#athena-gender-input').val());
        this.model.save(null, {
            headers: {'Authorization': 'JWT ' + token},
            error: function () {
                alert('上传错误');
                window.location.reload();
            },
            data: formData,
            patch: true,
            wait: true,
            emulateJSON: true,
            contentType: false,
            processData: false
        });
    }

});
```

在`events`中，指定了`input`元素发生变化时候的事件处理。在事件处理函数中，第一行我们给`imgFile`赋值。
其中还介绍了怎么打开一个图片并显示在`img`标签中。