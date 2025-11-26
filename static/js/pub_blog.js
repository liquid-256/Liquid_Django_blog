window.onload = function(){
    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        // 监听编辑行为
        onChange(editor) {
          const html = editor.getHtml()
          // 编辑器内容已更新
          // 也可以同步到 <textarea>
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function(event){
        event.preventDefault();

        let title = $("input[name='title']").val().trim();
        let category = $("#category-select").val();
        let content = editor.getHtml();
        let plainText = editor.getText().replace(/\s+/g, '');
        let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

        if(!title){
            alert('标题不能为空');
            return;
        }
        if(!plainText || plainText.length < 10){
            alert('内容至少需要10个字符');
            return;
        }

        $.ajax('/blog/pub',{
            method: 'POST',
            data: {title, category, content, csrfmiddlewaretoken},
            success: function(result){
                if(result['code'] == 200){
                    let blog_id = result['data']['blog_id'];
                    window.location = '/blog/detail/' + blog_id;
                }else{
                    alert(result['message']);
                }
            },
            error: function(xhr){
                alert(xhr.responseJSON && xhr.responseJSON.message ? xhr.responseJSON.message : '发布失败，请稍后重试');
            }
        })
    });
}