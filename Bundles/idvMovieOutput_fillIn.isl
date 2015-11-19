<isl debug="true" offscreen="false">
    <bundle clear="true" file="../BUNDLENAME.xidv" wait="true"></bundle>
    <movie file="MOVIENAME.mov">
        <overlay text="METADATA" place="lm,0,-10" anchor="lm" color="blue" fontsize="16"/>
    </movie>
    <image file="IMAGENAME.png">
        <resize width="200" height="200"/>
	<overlay text="METADATA" place="lm,0,-10" anchor="lm" color="blue" fontsize="8"/>
    </image>
    <displayproperties display="class:ucar.unidata.idv.control.ColorPlanViewControl">
        <property name="DisplayAreaSubset" value="true"/>
    </displayproperties>
    <export file="../BUNDLENAME.zidv" what="zidv"/>
</isl>