import os
import math
import unittest
import epanettools
from epanettools.examples import simple
from  epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
      Links, Patterns, Pattern, Controls, Control

from unittest import skip, expectedFailure


class Test1(unittest.TestCase):
    def setUp(self): 
        print("SETUP!")
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        self.es=EPANetSimulation(file)           
    
    def tearDown(self):
        self.es.clean()
        print("TEAR DOWN!")
    
    @skip  
    def test_false(self):
        assert False
        
    def test_epnetsimulation_has_a_network_which_has_nodes_and_links(self):
        self.assertIsInstance(self.es.network,Network)
        self.assertIsInstance(self.es.network.links,Links)
        self.assertIsInstance(self.es.network.nodes,Nodes)
        self.assertIsInstance(self.es.network.nodes[1],Node)
        self.assertIsInstance(self.es.network.links[1],Link)
        
    def test_network_has_patterns(self):
        self.assertIsInstance(self.es.network.patterns,Patterns)
        self.assertIsInstance(self.es.network.patterns[1],Pattern)
        self.assertEqual(len(self.es.network.patterns),5)
        self.assertEqual(self.es.network.patterns['4'][7],1777) # can call with index or...
        self.assertEqual(self.es.network.patterns[4][7],1777)   # id. And for specific value, call the item.

    def test_network_has_controls(self):
        self.assertIsInstance(self.es.network.controls,Controls)
        self.assertIsInstance(self.es.network.controls[1],Control)
        self.assertEqual(len(self.es.network.controls),6)
        c=[self.es.network.controls[x] for x in range(1,5)]
        self.assertEqual(c[0].link.id,'10')
        self.assertEqual(c[0].node,None)
        self.assertEqual(c[0].level,3600.)
        self.assertAlmostEqual(c[0].setting,Link.OPENED)
        self.assertEqual(c[0].ctype,Control.control_types['TIMER_CONTROL'])
        
        self.assertAlmostEqual(c[1].setting,Link.CLOSED)
        
        self.assertAlmostEqual(c[2].setting,Link.OPENED) #Link 335 OPEN IF Node 1 BELOW 17.1
        self.assertEqual(c[2].link.id,'335')
        self.assertEqual(c[2].node.id,'1')
        self.assertAlmostEqual(c[2].level,17.1,places=1)
        self.assertEqual(c[2].ctype,Control.control_types['LOW_LEVEL_CONTROL'])
        
        self.assertAlmostEqual(c[3].setting,Link.CLOSED) #Link 335 OPEN IF Node 1 BELOW 17.1
        self.assertEqual(c[3].link.id,'335')
        self.assertEqual(c[3].node.id,'1')
        self.assertAlmostEqual(c[3].level,19.1,places=1)
        self.assertEqual(c[3].ctype,Control.control_types['HIGH_LEVEL_CONTROL']) 
        
    def test_water_quality_analysis_type_is_set(self):
        self.assertEqual(self.es.network.WaterQualityAnalysisType,Network.WaterQualityAnalysisTypes["EN_TRACE"])
        self.assertEqual(self.es.network.WaterQualityTraceNode.id,'Lake')
        
    def test_proper_options_are_set(self):
        n=self.es.network
        self.assertAlmostEqual(n.en_accuracy,0.001,places=3)
        self.assertAlmostEqual(n.en_demandmult,1.0,places=3)
        self.assertAlmostEqual(n.en_emitexpon,0.5,places=2)
        self.assertAlmostEqual(n.en_tolerance,.01,places=5)
        self.assertAlmostEqual(n.en_trials,40.0,places=3)
       
        
    def test_can_import_EPANetSimulation(self):
        try:
            from epanettools.epanettools import EPANetSimulation
        except (Exception):
            assert False
            
    def test_non_existing_file_raise_error(self):
        self.assertRaises(FileNotFoundError, EPANetSimulation,"Silly file")
        
        
        
    def test_in_input_type_nodes_node_data_has_only_one_value(self):
        def mod1():
            for j,node in self.es.network.nodes.items():
                for t,i in Node.value_type.items():
                    if(not i in Node.settable_values):
                        continue
                    self.assertEqual(len(node.results[i]),1)
        mod1()        
        self.es.run()
        mod1()
        self.es.runq()
        mod1()
            
    def test_in_output_type_nodes_node_data_has_multiple_values(self):
        def mod1(before_run=True):
            for j,node in self.es.network.nodes.items():
                for t,i in Node.value_type.items():
                    if(i in Node.input_values):
                        continue
                    if(before_run):
                        self.assertEqual(len(node.results[i]),0)
                    else: 
                        self.assertEqual(len(node.results[i]),len(self.es.network.time))
        mod1()        
        self.es.run()
        mod1(False)
        self.es.runq()
        mod1(False)    
        
    def test_for_input_type_links_link_data_has_only_one_value(self):
        def mod1():
            for j,link in self.es.network.links.items():
                for t,i in Link.value_type.items():
                    if(not i in Link.settable_values):
                        continue
                    self.assertEqual(len(link.results[i]),1)
        mod1()        
        self.es.run()
        mod1()
        self.es.runq()
        mod1()
        
    def test_for_output_type_links_link_data_has_multiple_values(self):
        def mod1(before_run=True):
            for j,link in self.es.network.links.items():
                for t,i in Link.value_type.items():
                    if(i in Link.settable_values):
                        continue
                    if(before_run):
                        self.assertEqual(len(link.results[i]),0)
                    else: 
                        self.assertEqual(len(link.results[i]),len(self.es.network.time))
        mod1()        
        self.es.run()
        mod1(False)
        self.es.runq()
        mod1(False)
    
    
    def test_properly_open_a_network_file(self):
        import filecmp
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        es=EPANetSimulation(file)
        self.assertNotEqual(file,self.es.inputfile)
        self.assertTrue(os.path.isfile(self.es.inputfile))
        self.assertFalse(os.path.isdir(self.es.inputfile))
        # file names are unique
        self.assertEqual(len(set([EPANetSimulation(file).inputfile for i in range(100)])),100)
        # file content is identical to the original file
        self.assertTrue(filecmp.cmp(self.es.inputfile,file))
        # but names are not the same
        self.assertFalse(self.es.inputfile==file)
        
    def test_get_correct_network_information(self):
        n=self.es.network.nodes
        self.assertEqual(n[1].id,'10')
        self.assertEqual(n[3].id,'20')
        self.assertEqual(n[25].id,'129')
        self.assertEqual(n[94].id,'Lake')
        
        self.assertEqual(n[94].index,94)
        
        m=self.es.network.links
        self.assertEqual(m[1].id,'20')
        self.assertEqual(m[3].id,'50')
        self.assertEqual(m[119].id,'335')  
        self.assertEqual([m[1].start.id,m[1].end.id],['3','20'])
        self.assertEqual([m[118].start.id,m[118].end.id],['Lake','10'])
        
        # types of nodes
        self.assertEqual(n[94].node_type,Node.node_types['RESERVOIR'])
        self.assertEqual(n[1].node_type,Node.node_types['JUNCTION'])
        self.assertEqual(n['2'].node_type,Node.node_types['TANK'])
        
        #types of links
        self.assertEqual(m['335'].link_type,Link.link_types['PUMP'])
        self.assertEqual(m['101'].link_type,Link.link_types['PIPE'])
        self.assertEqual(m[1].link_type,Link.link_types['PIPE'])
        
        self.assertEqual(m[119].index,119)
        
        # link or node can be searched with ID too. 
        self.assertEqual(n['Lake'].id,'Lake')
        self.assertEqual(n['Lake'].index,94)
        self.assertEqual(m['335'].id,'335')
        self.assertEqual(m['335'].index,119)
        
        # get the links connected to a node. 
        self.assertEqual(sorted([i.id for i in n['169'].links]),['183', '185', '187', '211'] )
        
        

        
    def test_can_access_low_level_EN_type_functions(self):
        self.assertEqual(self.es.ENgetnodeid(3),[0,'20'])
        
        
    def test_each_node_and_link_has_the_epanetsimulation_object_linked_to_it_as_variable_es(self):
        self.assertIsInstance(self.es.network.links[1].network.es,EPANetSimulation)
        self.assertIsInstance(self.es.network.nodes[1].network.es,EPANetSimulation)
    
    def test_runs_a_simulation_and_get_results(self):
        def mod1():
            p=Node.value_type['EN_PRESSURE']
            self.assertAlmostEqual(self.es.network.nodes['103'].results[p][5],59.301,places=3)
            self.assertAlmostEqual(self.es.network.nodes['125'].results[p][5],66.051,places=3)
            self.assertEqual(self.es.network.time[5],15213)
            self.assertEqual(self.es.network.tsteps[5],2787)
            self.assertEqual(self.es.network.tsteps[6],3600)
            self.assertEqual(len(self.es.network.time),len(self.es.network.nodes[1].results[p]))
            
            d=Node.value_type['EN_DEMAND']
            h=Node.value_type['EN_HEAD']
            self.assertAlmostEqual(self.es.network.nodes['103'].results[d][5],101.232, places=3)
            self.assertAlmostEqual(self.es.network.nodes['103'].results[h][5],179.858, places=3)
        
        def mod2():
            p=Link.value_type['EN_DIAMETER']
            self.assertAlmostEquals(self.es.network.links[1].results[p][0],99.0,places=1) #index is not important. Diameter is fixed. !
            self.assertAlmostEquals(self.es.network.links['105'].results[p][0],12.0,places=1)
            v=Link.value_type['EN_VELOCITY']
            self.assertAlmostEquals(self.es.network.links[2].results[v][22],0.025,places=2)
            self.assertAlmostEquals(self.es.network.links['111'].results[v][1],3.23,places=2)
            
        self.es.run()
        mod1()
        mod2()
        self.es.runq()
        q=Node.value_type['EN_QUALITY']
        self.assertAlmostEqual(self.es.network.nodes['117'].results[q][4],85.317,places=3)
        self.assertAlmostEqual(self.es.network.nodes['117'].results[q][5],100.0)
        e=Link.value_type['EN_ENERGY']
        self.assertAlmostEquals(self.es.network.links['111'].results[e][23],.00685,places=2)
        mod1()
        mod2()
    
    def test_hydraulic_file_is_saved_only_when_save_is_true(self):
        self.es.run(save=False)
        self.assertFalse(os.path.exists(self.es.hydraulicfile))
        self.es.run(save=True)
        self.assertTrue(os.path.exists(self.es.hydraulicfile))        

    
    def test_clean_will_remove_results(self):
        self.assertTrue(os.path.exists(self.es.inputfile))        
        self.es.run()
        self.assertTrue(os.path.exists(self.es.rptfile))
        self.assertTrue(os.path.exists(self.es.hydraulicfile))         
        self.es.runq()
        self.assertTrue(os.path.exists(self.es.rptfile))
        self.assertTrue(os.path.exists(self.es.binfile))
        self.assertTrue(os.path.exists(self.es.hydraulicfile))         
        self.es.clean()
        self.assertTrue(os.path.exists(self.es.inputfile))
        self.assertFalse(os.path.exists(self.es.rptfile))
        self.assertFalse(os.path.exists(self.es.binfile))
        self.assertFalse(os.path.exists(self.es.hydraulicfile))
        
    def test_settable_values_for_links_and_nodes(self):
        self.assertEqual(Link.settable_values,[0,1,2,3,4,5,6,7,11,12])
        self.assertEqual(Node.settable_values,[0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 17, 18, 20, 21, 22, 23])
        
    def xtest_node_values_are_saved_when_synced(self):
        #change copule'a values
        d=Link.value_type['EN_DIAMETER']
        self.es.network.links[1].results[d][0]
        self.es.network.links[1].results[d][0]=152.0
        self.es.network.links['105'].results[d][0]=18.0    
        #first without 'syncing""
        self.assertAlmostEquals(self.es._legacy_get('LINK',1,d),99.0,places=1) 

        self.assertAlmostEquals(self.es._legacy_get('LINK',self.es.network.links['105'].index,d),12.0,places=1)
        #now after 'syncing'
        self.es.sync()
        self.assertAlmostEquals(self.es._legacy_get('LINK',1,d),152.0,places=1) 
        self.assertAlmostEquals(self.es._legacy_get('LINK',self.es.network.links['105'].index,d),18.0,places=1)
        # now run and get results
        self.es.run()
        self.assertAlmostEquals(self.es.network.links[1].results[Link.value_type["EN_FLOW"]][0],-2246.30,places=1)        
         
        
       
        
        
        

tc=Test1()
def clt(fn):
    tc.setUp()
    fn()
    tc.tearDown()

def main():
    for a in dir(tc):
        if (a.startswith('test_')):
            b=getattr(tc,a)
            if(hasattr(b, '__call__')):
                print ("calling %s **********************************" % a )
                clt(b)
           


if __name__ == "__main__":
        main()