document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".edit-btn").forEach(button => {
        const originalOnClick = button.onclick; 
        
        button.onclick = () => {
            const postId = button.dataset.postId;
            const postContent = document.querySelector(`.post-content[data-post-id='${postId}']`);
            
            // Crea el textarea
            const textarea = document.createElement("textarea");
            textarea.className = "form-control";
            textarea.value = postContent.innerHTML.trim();
            postContent.replaceWith(textarea);

            // Cambia el botón a "Guardar"
            button.innerText = "Save";
            button.onclick = () => {
                fetch(`/edit_post/${postId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({ content: textarea.value })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        // Reemplaza el contenido actualizado
                        const newContent = document.createElement("p");
                        newContent.className = "card-text post-content";
                        newContent.dataset.postId = postId;
                        newContent.innerHTML = textarea.value;
                        textarea.replaceWith(newContent);

                        // Restaura el botón y el evento original
                        button.innerText = "Edit";
                        button.onclick = originalOnClick;
                    }
                });
            };
        };
    });
});