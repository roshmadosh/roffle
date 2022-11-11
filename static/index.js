const contentEditable = document.querySelector("[contenteditable]")
const placeholder = document.getElementById("placeholder");

contentEditable.addEventListener("focusin", contentEditableEventHandler)
contentEditable.addEventListener("focusout", contentEditableEventHandler);

function contentEditableEventHandler(e) {
    const event = e.type

    switch (event) {
        case 'focusin':       
            if (!contentEditable.textContent) {
                placeholder.classList.add('invisible')
            } break;
        case 'focusout':
            if (!contentEditable.textContent) {
                placeholder.classList.remove('invisible')
            } break;
        default:
            break;
        }
}