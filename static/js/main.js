import { evaluateAction } from './mixins/api.js';
import { setModalWindow, removeModalWindow } from './mixins/modalWindow.js';

$(document).ready(() => {
    $('#current-year').text(new Date().getFullYear());

    const spinner = $('#spinner');

    $('#evaluate-btn').off('click').on('click', async (e) => {
        e.preventDefault();
        
        const code1 = $('#code1').val();
        const code2 = $('#code2').val();
        
        if (!code1 || !code2) return;
        
        spinner.removeClass('d-none').addClass('d-block');
    
        try {
            const response = await evaluateAction(code1, code2);
            const { status, err_description } = response;
            let { data } = response;
            
            if (!status) {
                throw Error(err_description);
            }

            if (typeof data === 'string') {
                data = JSON.parse(data);
            }

            const { score, advice } = data;

            const text = `Score: ${score}. ${advice}`;

            setModalWindow('SCORE AND ADVICE', text);
            
        } catch (e) {
            alert(e.message ?? 'Something went wrong');
        } finally {
            spinner.removeClass('d-block').addClass('d-none');
        }
    })

    $('#close-modal-btn').off('click').on('click', (e) => {
        e.preventDefault();

        removeModalWindow();
    })
})