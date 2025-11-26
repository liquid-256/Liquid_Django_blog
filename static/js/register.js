$(function(){
    function bindCaptchaBtnClick(){
        $("#captcha-btn").click(function(event){
            let $this = $(this);
            let email = $("input[name='email']").val();
            if(!email){
                alert("请先输入邮箱！");
                return;
            }
            // 取消按钮的点击事件
            $this.off('click');

            // 发送 ajax 请求
            $.ajax('/auth/captcha?email='+email, {
                method: 'GET',
                success: function(result){
                    if(result['code'] == 200){
                        alert("验证码发送成功！");
                    }else{
                        alert(result['message']);
                    }
                },
                error: function(error){
                    // 验证码发送失败，错误信息已在 alert 中显示
                }
            })

            // 倒计时
            let countdown = 60;
            let timer = setInterval(function(){
                if(countdown<=0){
                    $this.text('获取验证码');
                    // 清掉定时器
                    clearInterval(timer);
                    // 重新绑定点击事件
                    bindCaptchaBtnClick();
                }else{
                    countdown--;
                    $this.text(countdown+"s")
                }
            }, 1000);
        })
    }
    bindCaptchaBtnClick();
});