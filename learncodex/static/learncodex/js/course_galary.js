$(document).ready(function () {
    let viewport = getViewport()
    let debounce
    $(window).resize(() => {
      debounce = setTimeout(() => {
        const currentViewport = getViewport()
        if (currentViewport !== viewport) {
          viewport = currentViewport
          $(window).trigger('newViewport', viewport)
        }
      }, 500)
    })
    $(window).on('newViewport', (viewport) => {

        console.log(viewport)
        const screen = getViewport()
        console.log(screen)
      if(screen == 'sm' || screen == 'xs')
      {
          $('#discription').collapse('toggle')
          $('.content').css('margin-left','0px')
          $('.content').css('margin-right','0px')
          console.log(screen)
      }
      else{
        $('#discription').collapse('show')
        $('.content').css('margin-left','15px')
        $('.content').css('margin-right','-15px')
      }
      
    })
    // run when page loads
    $(window).trigger('newViewport', viewport)

    $('.plyr').addClass('img-fluid')
    $('.plyr').addClass('w-100')
  })

  function getViewport () {
    // https://stackoverflow.com/a/8876069
    const width = Math.max(
      document.documentElement.clientWidth,
      window.innerWidth || 0
    )
    if (width <= 576) return 'xs'
    if (width <= 768) return 'sm'
    if (width <= 992) return 'md'
    if (width <= 1200) return 'lg'
    return 'xl'
  }