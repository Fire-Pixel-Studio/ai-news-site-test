document.addEventListener("DOMContentLoaded", () => {
    fetchNews();
});

function fetchNews(query = "") {
    let url = "/api/news";
    if (query) url += `?q=${encodeURIComponent(query)}`;
    document.getElementById("newsContainer").innerHTML = "<p>Loading AI-powered news...</p>";
    fetch(url)
        .then(res => res.json())
        .then(news => {
            const container = document.getElementById("newsContainer");
            container.innerHTML = "";
            if (news.length === 0) {
                container.innerHTML = "<p>No news found.</p>";
                return;
            }
            news.forEach(item => {
                const card = document.createElement("div");
                card.className = "news-card";
                card.innerHTML = `
                    <img class="news-image" src="${item.image || '/static/placeholder.jpg'}" alt="news">
                    <div class="news-content">
                        <a href="${item.url}" class="news-title" target="_blank">${item.title}</a>
                        <p class="news-summary">${item.summary}</p>
                    </div>
                `;
                container.appendChild(card);
            });
        });
}

window.searchNews = function() {
    const query = document.getElementById("searchInput").value.trim();
    fetchNews(query);
};
