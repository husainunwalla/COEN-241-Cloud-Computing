# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This component is for use with the OpenFlow tutorial.

It acts as a simple hub, but can be modified to act like an L2
learning switch.

It's roughly similar to the one Brandon Heller did for NOX.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()



class Tutorial (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection
    self.trafficCount=0 #counts amount of packets seen on this switch
    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}


  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)


  def act_like_hub (self, packet, packet_in):
    """
    Implement hub-like behavior -- send all packets to all ports besides
    the input port.
    """

    # We want to output to all ports -- we do that using the special
    # OFPP_ALL port as the output port.  (We could have also used
    # OFPP_FLOOD.)
    self.resend_packet(packet_in, of.OFPP_ALL)

    # Note that if we didn't get a valid buffer_id, a slightly better
    # implementation would check that we got the full data before
    # sending it (len(packet_in.data) should be == packet_in.total_len)).


  def act_like_switch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """
    #Learn the port for the source MAC
    #print("Src: ",str(packet.src),":",packet_in.in_port,"Dst:",str(packet.dst))
    if packet.src not in self.mac_to_port:
        #print("Learning that " + str(packet.src) + " is attached at port " + str(packet_in.in_port))
        self.mac_to_port[packet.src]=packet_in.in_port

    #if the port associated with the destination MAC of the packet is known:
    if packet.dst in self.mac_to_port:
      # Send packet out the associated port
      #print(str(packet.dst) + " destination known. only send message to it")
      self.resend_packet(packet_in, self.mac_to_port[packet.dst])
    else:
        #print(str(packet.dst) + " not known, broadcast to all")
        self.resend_packet(packet_in,of.OFPP_ALL)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
    self.trafficCount=self.trafficCount+1
    packet_in = event.ofp # The actual ofp_packet_in message.

    #ADDITIONS FOR TASK 2 Q4: printng self to check what switches are handling packets and trafficCount to check how many packets have been seen
    #print(self.connection)
    #print(self.trafficCount)

    # Comment out the following line and uncomment the one after
    # when starting the exercise.
    #NOTE: CHANGED this function from act_like_hub to act_like_switch to change the function
    self.act_like_switch(packet, packet_in)
    #self.act_like_switch(packet, packet_in)



def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)