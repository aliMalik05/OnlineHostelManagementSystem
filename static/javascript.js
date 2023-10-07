const counters = document.querySelectorAll('.counter');

console.log(counters)




window.onscroll= function()
{
    myFunction()
};


function myFunction(){
    if (document.documentElement.scrollTop>1500)
    {
        counters.forEach((counter)=>{
    counter.innerHTML = 0;
    const updateCounter = ()=>{
        const target = counter.getAttribute('data-target');
        console.log(target);
        const targetNum = Number(target);
        const increment = targetNum/100;
        const startNum = Number(counter.innerHTML);
        if (startNum < targetNum)
        {
            counter.innerHTML = Math.round(startNum + increment);
            setTimeout(updateCounter , 10);
        }
        else
        {
            counter.innerHTML = targetNum;
        }
    }
    updateCounter();
})

    window.onscroll=null;
    }
}