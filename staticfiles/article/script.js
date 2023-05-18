const upvote = document.getElementById("upvote");
const downvote = document.getElementById("downvote");
const vote_count = document.getElementById("vote-count");
const upvoteBtn = document.getElementById("upvote-href");
const downvoteBtn = document.getElementById("downvote-href");

function getCookie(name) {
  const cookieValue = document.cookie.match(
    "(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"
  );
  return cookieValue ? cookieValue.pop() : "";
}

function vote_func(event, upvote) {
  event.preventDefault();
  const csrftoken = getCookie("csrftoken");
  const postId = upvoteBtn.getAttribute("data-post-id");
  const url = upvote ? `/post/${postId}/upvote/` : `/post/${postId}/downvote/`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // update vote count
      vote_count.textContent = data["vote-count"];
    })
    .catch((error) => {
      console.log(error);
    });
}

upvote.addEventListener("click", function (event) {
  if (
    !downvote.classList.contains("downvote") &&
    !upvote.classList.contains("upvote")
  ) {
    upvote.classList.toggle("upvote");
  } else if (
    !downvote.classList.contains("downvote") &&
    upvote.classList.contains("upvote")
  ) {
    upvote.classList.toggle("upvote");
  } else if (downvote.classList.contains("downvote")) {
    downvote.classList.toggle("downvote");
    upvote.classList.toggle("upvote");
  }
  vote_func(event, true);
});
downvote.addEventListener("click", function (event) {
  if (
    !upvote.classList.contains("upvote") &&
    !downvote.classList.contains("downvote")
  ) {
    downvote.classList.toggle("downvote");
  } else if (
    !upvote.classList.contains("upvote") &&
    downvote.classList.contains("downvote")
  ) {
    downvote.classList.toggle("downvote");
  } else if (upvote.classList.contains("upvote")) {
    upvote.classList.toggle("upvote");
    downvote.classList.toggle("downvote");
  }
  vote_func(event, false);
});
