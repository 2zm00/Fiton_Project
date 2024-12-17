document.addEventListener('DOMContentLoaded', function () {
    // id가 #id_role값을 가진 select요소를 role에 저장
    const role = document.querySelector('#id_role');
    //select값에 따라 변경될 id가 who인 필드
    const who = document.getElementById('who');
    
    if (role) {
        //role이 change 되면
        role.addEventListener('change', function () {
            // 선택된 role 값
            const selectedRole = role.value;

            // CSRF 토큰 가져오기
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // axios 설정
            axios.defaults.xsrfHeaderName = 'X-CSRFToken';
            axios.defaults.xsrfCookieName = 'csrftoken';

            // axios로 서버에 POST요청을 selectedRole데이터를 포함해 보낸다
            axios.post('/signup/choice/', { role: selectedRole }, {
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                // 서버로부터 렌더링된 HTML을 받아와 업데이트
                who.innerHTML = response.data.rendered_form;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('오류가 발생했습니다. 다시 시도해주세요.');
            });
        });
    }
});
