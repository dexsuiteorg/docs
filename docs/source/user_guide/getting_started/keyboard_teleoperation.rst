.. include:: ../_shared_nav.rst
Keyboard Teleoperation
===========

Try out our simple teleoperation setup - with just your keyboard! To launch the demo, invoke the example using bash or zsh. This table contains a simple Franka arm and a Robotiq gripper.

Run Script
----------
.. code-block:: bash

   # from the repository root (contains the "dexsuite/" folder)
   python dexsuite/examples/keyboard_demo.py

   # or
   python -m dexsuite.examples.keyboard_demo

Refer to the movement control tables below for key bindings.

Camera and System Controls
-----------------
+---------------+------------------+
| Key           | Action           |
+===============+==================+
| :kbd:`i`      | show information |
+---------------+------------------+
| :kbd:`r`      | record video     |
+---------------+------------------+
| :kbd:`s`      | save image       |
+---------------+------------------+
| :kbd:`z`      | reset camera     |
+---------------+------------------+
| :kbd:`a`      | camera rotation  |
+---------------+------------------+
| :kbd:`h`      | shadow           |
+---------------+------------------+
| :kbd:`f`      | face normal      |
+---------------+------------------+
| :kbd:`v`      | vertex normal    |
+---------------+------------------+
| :kbd:`w`      | world frame      |
+---------------+------------------+
| :kbd:`l`      | link frame       |
+---------------+------------------+
| :kbd:`d`      | wireframe        |
+---------------+------------------+
| :kbd:`c`      | camera & frustrum|
+---------------+------------------+
| :kbd:`q`      | quit             |
+---------------+------------------+

Movement Controls
-----------------
+---------------+------------------+
| Key           | Action           |
+===============+==================+
| :kbd:`h`      | ``+`` roll       |
+---------------+------------------+
| :kbd:`k`      | ``-`` roll       |
+---------------+------------------+
| :kbd:`y`      | ``+`` pitch      |
+---------------+------------------+
| :kbd:`g`      | ``-`` pitch      |
+---------------+------------------+
| :kbd:`b`      | ``+`` yaw        |
+---------------+------------------+
| :kbd:`n`      | ``-`` yaw        |
+---------------+------------------+
| :kbd:`o`      | open gripper     |
+---------------+------------------+
| :kbd:`p`      | close gripper    |
+---------------+------------------+

Bimanual Controls
-----------------
+---------------+--------------------+
| Key           | Action             |
+===============+====================+
| :kbd:`u`      | left gripper open  |
+---------------+--------------------+ 
| :kbd:`j`      | left gripper close |
+---------------+--------------------+
| :kbd:`o`      | right gripper open |
+---------------+--------------------+
| :kbd:`p`      | right gripper close|
+---------------+--------------------+
| :kbd:`num 0`  | open both grippers |
+---------------+--------------------+
| :kbd:`h`      | left arm ``+`` x   |
+---------------+--------------------+
| :kbd:`n`      | left arm ``-`` x   |
+---------------+--------------------+
| :kbd:`b`      | left arm ``+`` y   |
+---------------+--------------------+
| :kbd:`m`      | left arm ``-`` y   |  
+---------------+--------------------+
| :kbd:`→`      | right arm ``+`` x  |
+---------------+--------------------+
| :kbd:`←`      | right arm ``-`` x  |
+---------------+--------------------+
| :kbd:`↑`      | right arm ``+`` y  |
+---------------+--------------------+
| :kbd:`↓`      | right arm ``-`` y  |  
+---------------+--------------------+
