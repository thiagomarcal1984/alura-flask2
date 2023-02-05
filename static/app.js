// Código antigo, com jQuery.
// $('form input[type="file"]').change(event => {
//   let arquivos = event.target.files;
//   if (arquivos.length === 0) {
//     console.log('sem imagem pra mostrar')
//   } else {
//       if(arquivos[0].type == 'image/jpeg') {
//         $('img').remove();
//         let imagem = $('<img class="img-fluid">');
//         imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
//         $('figure').prepend(imagem);
//       } else {
//         alert('Formato não suportado')
//       }
//   }
// });

// Código novo, sem jQuery.
document.querySelector('form input[type="file"]').onchange = (event) => {
  let arquivos = event.target.files;
  if (arquivos.length === 0) {
    console.log('sem imagem pra mostrar')
  } else {
      // if(arquivos[0].type == 'image/jpeg') { // Código original só permite jpeg.
      if(arquivos[0].type.startsWith('image/')) {
        document.querySelector('img').remove();
        let imagem = document.createElement('img');
        imagem.classList.add('img-fluid');
        imagem.setAttribute('src', window.URL.createObjectURL(arquivos[0]));
        document.querySelector('figure').prepend(imagem);
      } else {
        alert('Formato não suportado')
      }
  }
};
