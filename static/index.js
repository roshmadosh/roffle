let contentEditable = document.getElementById("line1")
const placeholder = document.getElementById("placeholder");


let line_number = 1;

contentEditable.addEventListener("focusin", contentEditableEventHandler);
contentEditable.addEventListener("focusout", contentEditableEventHandler);
contentEditable.addEventListener("keydown", contentEditableEventHandler);


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

        case 'keydown':
            const textEditor = document.getElementById('text-editor');
            const max_width = textEditor.offsetWidth * .87;

            if (contentEditable.offsetWidth > max_width || e.key === 'Enter') {
                e.preventDefault();
                line_number++
                textEditor.innerHTML += `<br><span contentEditable="true" id="line${line_number}"></span>`
                contentEditable = document.getElementById(`line${line_number}`);
                contentEditable.addEventListener("keydown", contentEditableEventHandler);
                contentEditable.focus()
            }


        default:
            break;
        }
}