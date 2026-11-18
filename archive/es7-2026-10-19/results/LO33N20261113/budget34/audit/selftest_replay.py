"""Small adversarial controls of the new wrapper; no real tree is searched."""
import copy
import json
from replay34 import frontier,envelope,descriptor,check_tree,dump,AUDIT


def rejected(fn):
    try:
        fn()
    except (AssertionError,ValueError,KeyError,TypeError,IndexError):
        return True
    raise AssertionError('deliberately invalid packet was accepted')


def main():
    master={'root':0,'contexts':2,'master_leaves':0,'nodes':[
        {'type':'branch','vertex':1,'zero':1,'one':2},
        {'type':'context','context':0},{'type':'context','context':1}]}
    paths=frontier(master)
    assert paths=={0:((0,0),(1,0)),1:((0,0),(1,1))}
    tests={}
    for name,edit in [
        ('duplicate_context',lambda m:m['nodes'][2].update(context=0)),
        ('repeated_state0',lambda m:m['nodes'][0].update(vertex=0)),
        ('invalid_child',lambda m:m['nodes'][0].update(one=9)),
        ('shared_child',lambda m:m['nodes'][0].update(one=1)),
        ('unreachable_node',lambda m:m['nodes'].append({'type':'context','context':2})),
        ('pending_master',lambda m:m['nodes'][1].update(type='pending')),
        ('wrong_context_count',lambda m:m.update(contexts=1)),
        ('bool_vertex',lambda m:m['nodes'][0].update(vertex=True))]:
        m=copy.deepcopy(master);edit(m);tests[name]=rejected(lambda:frontier(m))
    tests['wrong_stored_path']=rejected(lambda:descriptor({'context':0,'missing':[1],'occupied':[0]},0,paths[0]))
    tests['duplicate_stored_state']=rejected(lambda:descriptor({'context':0,'missing':[],'occupied':[0,0,1]},0,paths[0]))
    tests['pending_subtree']=rejected(lambda:envelope([{'type':'pending'}],0,((0,0),)))
    rows=[(list(range(154)),35)]
    weighted=[{'type':'weighted','capacity':1,'weights':[[0,1]]}]
    wrapped,_=envelope(weighted,0,((0,0),))
    good=check_tree(154,rows,34,wrapped,0,allow_pending=True)
    assert good['minimum_margin']==1 and good['pending']==1
    tests['budget_off_by_one']=rejected(lambda:check_tree(154,rows,35,wrapped,0,allow_pending=True))
    tests['invalid_over_budget']=rejected(lambda:check_tree(154,rows,34,[{'type':'over_budget'}],0))
    result={'label':'COMPUTED wrapper controls','positive_budget34_margin':1,
            'deliberate_corruptions_rejected':tests,'passed':len(tests),'failed':0}
    dump(AUDIT/'wrapper_controls.json',result);print(json.dumps(result))


if __name__=='__main__':
    main()
