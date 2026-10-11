const BODY = $('body');

export const setModalWindow = (title, text) => {
    removeModalWindow();

    const modalWindow = $(`
        <div
            class="modal fade"
            id="staticBackdrop"
            data-bs-backdrop="static"
            data-bs-keyboard="false"
            tabindex="-1"
            aria-labelledby="staticBackdropLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1
                            class="modal-title fs-5"
                            id="staticBackdropLabel"
                        ></h1>

                        <button
                            id="close-modal-btn
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>

                    <div class="modal-body m-0"></div>
                </div>
            </div>
        </div>
    `);

    modalWindow.find('.modal-title').text(title);
    modalWindow.find('.modal-body').text(text);

    BODY.append(modalWindow);

    const modal = new bootstrap.Modal(
        modalWindow[0]
    );

    modalWindow.on('hidden.bs.modal', () => {
        modal.dispose();
        modalWindow.remove();
    });

    modal.show();

    return modal;
};

export const removeModalWindow = () => {
    $('.modal').each(function () {
        const modalInstance = bootstrap.Modal.getInstance(this);

        if (modalInstance) {
            modalInstance.dispose();
        }

        $(this).remove();
    });

    $('.modal-backdrop').remove();
    BODY.removeClass('modal-open');
    BODY.css('overflow', '');
    BODY.css('padding-right', '');
};