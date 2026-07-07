<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="17008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">17.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str">Created IvanLis by LabVIEW Portal
Profile: http://labviewportal.org/memberlist.php?mode=viewprofile&amp;u=987
eMail: IvanLisanov@gMail.com
Telegram: https://t.me/IvanLis</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="ONNX model" Type="Folder">
			<Item Name="ar.onnx" Type="Document" URL="../ONNX model/ar.onnx"/>
			<Item Name="coin_angle_detection.onnx" Type="Document" URL="../ONNX model/coin_angle_detection.onnx"/>
			<Item Name="coins_detection.onnx" Type="Document" URL="../ONNX model/coins_detection.onnx"/>
			<Item Name="Xiaolei Hu model.onnx" Type="Document" URL="../ONNX model/Xiaolei Hu model.onnx"/>
		</Item>
		<Item Name="onnx_wrapper" Type="Folder">
			<Item Name="libonnx_code" Type="Folder">
				<Item Name="unix64" Type="Folder">
					<Item Name="wrapper.cpp" Type="Document" URL="../onnx_wrapper/libonnx_code/unix64/wrapper.cpp"/>
					<Item Name="wrapper.h" Type="Document" URL="../onnx_wrapper/libonnx_code/unix64/wrapper.h"/>
				</Item>
				<Item Name="win64" Type="Folder">
					<Item Name="wrapper.cpp" Type="Document" URL="../onnx_wrapper/libonnx_code/win64/wrapper.cpp"/>
					<Item Name="wrapper.h" Type="Document" URL="../onnx_wrapper/libonnx_code/win64/wrapper.h"/>
				</Item>
				<Item Name="wrapper.h" Type="Document" URL="../onnx_wrapper/libonnx_code/wrapper.h"/>
			</Item>
			<Item Name="unix64" Type="Folder">
				<Item Name="libonnx_wrapper.so" Type="Document" URL="../onnx_wrapper/unix64/libonnx_wrapper.so"/>
				<Item Name="libonnxruntime.so" Type="Document" URL="../onnx_wrapper/unix64/libonnxruntime.so"/>
				<Item Name="libonnxruntime_providers_shared.so" Type="Document" URL="../onnx_wrapper/unix64/libonnxruntime_providers_shared.so"/>
			</Item>
			<Item Name="win64" Type="Folder">
				<Item Name="libonnx_wrapper.dll" Type="Document" URL="../onnx_wrapper/win64/libonnx_wrapper.dll"/>
				<Item Name="onnxruntime.dll" Type="Document" URL="../onnx_wrapper/win64/onnxruntime.dll"/>
				<Item Name="onnxruntime_providers_shared.dll" Type="Document" URL="../onnx_wrapper/win64/onnxruntime_providers_shared.dll"/>
			</Item>
		</Item>
		<Item Name="ONNX Class Library.lvlib" Type="Library" URL="../ONNX Class/ONNX Class Library.lvlib"/>
		<Item Name="ONNX YOLO Class Library.lvlib" Type="Library" URL="../ONNX YOLO Class/ONNX YOLO Class Library.lvlib"/>
		<Item Name="ONNX Angle Class Library.lvlib" Type="Library" URL="../ONNX Angle Class/ONNX Angle Class Library.lvlib"/>
		<Item Name="ONNX EfficientNet Class Library.lvlib" Type="Library" URL="../ONNX EfficientNet Class/ONNX EfficientNet Class Library.lvlib"/>
		<Item Name="libonnx_wrapper.lvlib" Type="Library" URL="../libonnx_wrapper/libonnx_wrapper.lvlib"/>
		<Item Name="image.lvlib" Type="Library" URL="../image_vi/image.lvlib"/>
		<Item Name="process_Angle.lvlib" Type="Library" URL="../process_Angle/process_Angle.lvlib"/>
		<Item Name="process_EfficientNet_B4.lvlib" Type="Library" URL="../process_EfficientNet_B4/process_EfficientNet_B4.lvlib"/>
		<Item Name="process_YOLOv8.lvlib" Type="Library" URL="../process_YOLOv8/process_YOLOv8.lvlib"/>
		<Item Name="Ivan_method.vi" Type="VI" URL="../Ivan_method.vi"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
