# PRPA_Practica2

1. Invariante:

2. Seguridad:

La seguridad se cumple debido a los Condition **CarCross** y **PedestrianCross**.

En el caso de los coches, asegura que no viene otro desde la otra direccion y que no haya
peatones. La funcion usada es **can_south** o **can_north**, dependiendo de la direccion en que venga.

En el caso de los peatones, asegura que no vienen coches. La función usada es
**can_pedestrian**.

3. Ausencia de Deadlocks:


4. Ausencia de inanicion:

En este caso la inanicion se asegura ya que el numero de peatones y coches es finito.
Aun asi, en caso de que haya cantidad alta de ambos se quedarían bloqueados hasta
que uno tipo acabase.


-------------Entrega2_v1--------------

Primera version, no limite de tamaño en el puente.

Suelen pasar todos los de un tipo a la vez.

--------------------------------------


