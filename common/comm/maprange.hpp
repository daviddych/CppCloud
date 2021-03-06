/*-------------------------------------------------------------------------
FileName     : maprange.hpp
Description  : 查找std::map中某个区间的元素
remark       : 使调用者简化编码
Modification :
--------------------------------------------------------------------------
   1、Date  2018-09-13       create     hejl 
-------------------------------------------------------------------------*/
#include <map>

/* *******************************************************
 * 使用示例
map<std::string, int> custommap;

custommap["hejl501"] =  1;
custommap["he021"] = 2;
custommap["ttt101"] = 3;
custommap["hojl101"] = 4;
custommap["hop107"] = 5;
custommap["hojl9101"] = 6;

MapRanger<std::string, int> cus(custommap, "ho", "ho~"); // 查询以"ho"开头的key对应的对象
while(cus.pop())
{
    printf("key=%s, val=%d\n", cus.retKey.c_str(), cus.retVal);
}

//////////// Output: //////////////
key=hojl101, val=4
key=hojl9101, val=6
key=hop107, val=5

*********************************************************/



using std::map;

template<class MPKEY, class MPVAL>
class MapRanger
{
public:
    MPKEY retKey;
    MPVAL retVal;
    MPKEY lower, upper;

    typedef typename std::map<MPKEY, MPVAL> AliasContainer;
    typedef typename AliasContainer::iterator AliasIterator;
    AliasContainer& contn;
    AliasIterator it0;
    AliasIterator it1;
    bool firstPop;


    MapRanger(AliasContainer& container, const MPKEY& k0 ): 
        lower(k0), contn(container), firstPop(true) 
    {
        it0 = contn.lower_bound(lower);
        it1 = contn.end();
    }

    MapRanger(AliasContainer& container, const MPKEY& k0, const MPKEY& k1 ): 
        lower(k0), upper(k1), contn(container), firstPop(true) 
    {
        it0 = contn.lower_bound(lower);
        it1 = contn.upper_bound(upper);
    }

    // param: forceFindEach是否每一次pop()都进行查找，当pop()得到的对象会可能被删除的情况要传true
    MPVAL pop(bool forceFindEach=false)
    {
        MPVAL ret = NULL;
        if (forceFindEach && !firstPop)
        {
            it0 = contn.upper_bound(retKey);
        }
        if (it0 != contn.end() && it0 != it1)
        {
            ret = (it0->second);
            retKey = it0->first;
            retVal = it0->second;
            ++it0;
            firstPop = false;
        }

        return ret;
    }

    bool empty(void)
    {
        return !(it0 != contn.end() && it0 != it1);
    }
};