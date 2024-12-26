let timeoutId;
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');

searchInput.addEventListener('input', function(e) {
    clearTimeout(timeoutId);
    
    timeoutId = setTimeout(() => {
        const query = e.target.value;
        if (query.length >= 2) {
            fetchSearchResults(query);
        } else {
            searchResults.classList.add('hidden');
        }
    }, 300);
});

async function fetchSearchResults(query) {
    try {
        const response = await fetch(`/search/?q=${query}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        const data = await response.json();
        updateSearchResults(data.results);
    } catch (error) {
        console.error('검색 중 오류 발생:', error);
    }
}

function updateSearchResults(results) {
    searchResults.innerHTML = '';
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="p-4 text-gray-500">검색 결과가 없습니다.</div>';
    } else {
        results.forEach(result => {
            const exercises = result.exercises.join(', ');
            searchResults.innerHTML += `
                <div class="p-4 hover:bg-gray-100 cursor-pointer" 
                     onclick="location.href='/center/${result.id}'">
                    <h3 class="font-bold">${result.name}</h3>
                    <p class="text-sm text-gray-600">${result.location}</p>
                    <p class="text-xs text-gray-500">${exercises}</p>
                </div>
            `;
        });
    }
    
    searchResults.classList.remove('hidden');
}

document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.add('hidden');
    }
});
