CloudCpp:=switchhand.cpp exception.cpp svrprop.cpp
SrcCpp:=climanage.cpp flowctrl.cpp listen.cpp iohand.cpp begn_hand.cpp query_hand.cpp act_mgr.cpp clibase.cpp
SrcCpp+=cppcloud_config.cpp main.cpp peer_serv.cpp peer_cli.cpp  hocfg_mgr.cpp 
SrcCpp+=peer_mgr.cpp outer_serv.cpp outer_cli.cpp keepaliver.cpp broadcastcli.cpp route_exchange.cpp 
SrcCpp+=service_provider.cpp provider_manage.cpp

TARGET=cppcloud_serv
INSTALLDIR:=/usr/local/bin

MKLLOGFILE:=make.log
ifeq ($(LOG2STD), 1) 
CONF_HEAD_INC+=-DLOG2STDOUT#日志输出至标准输出
endif

LIBCOMMON=../common

INCLUDEDIR+=-I.. -I$(LIBCOMMON) 
CXX=g++
CXXFLAGS=-Wall -g -std=c++11 -fPIC
#AR=ar rcs

CPPFLAGS+=$(CONF_HEAD_INC) $(INCLUDEDIR)
LDFLAGS=-Wall
LDLIBS=

ALIBS=

# 以下是使用静态库时选项
LOADLIBES+=-L/usr/local/lib -L$(LIBCOMMON) -Wl,-rpath,.
LDLIBS+=-lhocomm -lpthread #-lcrypto # CppCloud底层动态库

SRC=$(SrcCpp) $(CloudCpp:%.cpp=../common/cloud/%.cpp)
OBJ=$(SRC:.cpp=.o) 

# linking operation from *.o and lib.
$(TARGET): $(OBJ)
	$(CXX) $(LDFLAGS) $^ -o $@ $(LOADLIBES) $(LDLIBS) $(ALIBS)

install:
	@install -d $(INSTALLDIR)
	@install -p -s -t $(INSTALLDIR) $(TARGET)
	@echo "installed $(TARGET) to $(INSTALLDIR)"

uninstall:
	rm -f $(INSTALLDIR)/$(TARGET)
	@echo "uninstalled $(INSTALLDIR)/$(TARGET)"

	
vpc1:
	scp $(TARGET) hejl@vpc1:/home/hejl/test/cppcloud/$(TARGET)

# ---------------------------------------- #
sinclude .depend
.PHONY: clean depend
clean:
	@rm -rf $(TARGET) $(OBJ) $(COMMON_OBJ) $(LINKNAME)
cleanall:
	@rm -rf $(TARGET) $(OBJ) $(COMMON_OBJ) $(LINKNAME)
	@rm .depend

depend: $(SRC)
	$(CXX) -MM -std=c++11 $< $(INCLUDEDIR) $^ > .depend

