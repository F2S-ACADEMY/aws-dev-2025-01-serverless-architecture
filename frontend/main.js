document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("books-container");
  
    try {
      const res = await fetch(API_URL, {
        method: "GET",
        headers: { "x-api-key": API_KEY }
      });
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const books = await res.json();
  
      if (books.length === 0) {
        container.innerHTML = "<p class='text-gray-600'>Nenhum livro encontrado.</p>";
        return;
      }
  
      books.forEach(book => {
        const card = document.createElement("div");
        card.className = [
          "bg-white",
          "rounded-xl",
          "shadow-lg",
          "p-6",
          "transition-transform",
          "hover:scale-105",
          "flex",
          "flex-col",
          "items-center"
        ].join(" ");
        card.innerHTML = `
          <h3 class="text-xl font-bold text-blue-700 mb-2">${book.title}</h3>
          <p class="text-gray-700 mb-1"><strong>Autor:</strong> ${book.author}</p>
          <p class="text-gray-500 text-sm mb-4"><strong>ID:</strong> ${book.id}</p>
          <img src="default-cover.png" alt="Capa padrão" class="w-full h-48 object-cover rounded-lg mb-2" />
        `;
        container.appendChild(card);
      });
    } catch (err) {
      container.innerHTML = `<p class="text-red-600">Erro: ${err.message}</p>`;
    }
  });