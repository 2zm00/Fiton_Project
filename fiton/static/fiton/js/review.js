document.getElementById('submit-review-form').addEventListener('submit', function(event) {
    event.preventDefault(); // 기본 제출 방지

    const formData = new FormData(this); // 폼 데이터 생성
    const classId = this.dataset.classId; // 클래스 ID 가져오기
    
    fetch(`/class/${classId}/riview/create/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken') // CSRF 토큰 추가
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('리뷰를 저장하는 중 오류가 발생했습니다.');
        } else {
            // 새로운 리뷰를 추가
            const newReviewHTML = `
                <li class="review-item">
                    <p><strong>작성자:</strong> ${data.author}</p>
                    <p><strong>평점:</strong> ${data.rating}</p>
                    <p><strong>내용:</strong> ${data.comment}</p>
                    <p><strong>작성일:</strong> ${data.created_at}</p>
                    {% if request.user.id == review.member.user.id %}
                    <a href=" {% url 'fiton:review_modify' review.id %} ">수정</a>
                    <a href=" {% url 'fiton:review_delete' review.id %} ">삭제</a>
                    {% endif %}
                </li>
                
            `;
            document.getElementById('review-list').insertAdjacentHTML('afterbegin', newReviewHTML);
            document.getElementById('submit-review-form').reset(); // 폼 초기화
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('리뷰를 저장하는 중 오류가 발생했습니다.');
    });
});