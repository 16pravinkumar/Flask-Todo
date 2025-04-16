function showFlashMessage(message) {
  const flash = document.getElementById("flash-message");
  document.getElementById("flash-text").textContent = message;
  flash.classList.remove("hidden");
  flash.classList.add("opacity-100");

  setTimeout(() => {
    flash.classList.add("hidden");
  }, 3000);
}

function deleteTodo(sno) {
  fetch(`/delete/${sno}`, {
    method: "DELETE",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        document.getElementById(`todo-${sno}`)?.remove();
        if (document.querySelectorAll("tbody tr").length === 0) {
          document.getElementById("display-elements").innerHTML =
            '<p class="text-center text-gray-500 dark:text-gray-400">No items found</p>';
        }
        showFlashMessage("Data deleted successfully!");
      }
    });
}

setTimeout(() => {
  document.getElementById("flash-messages").style.display = "none";
}, 3000);


