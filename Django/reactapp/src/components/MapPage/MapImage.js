const MapImage = (props) => {
  console.log(props.mapLink);
  return (
    <div className="bg-slate-400 shadow-2xl rounded-lg px-8 pt-6 pb-8 mr-5">
      <img src="https://miro.medium.com/max/600/1*3A3r0f83LH7bZQGPEweXmQ.png" width='100%'/>
    </div>
  );
};

export default MapImage;
