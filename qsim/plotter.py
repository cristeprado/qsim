import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib.widgets import Slider, RadioButtons
from matplotlib.colors import colorConverter

class Plotter(object):

    def __init__(self, sim):
        self.sim = sim
        self.dm = self.sim.steps
        self.N_h, self.N_vi = self.sim.steps[0].H_h_vi.shape
        print self.N_h
        print self.N_vi

    def plot(self):
        print "Plotting..."

        plot_var="H_h_vi"
        t_init=0
        t=t_init
        ds=self.dm[t]
        data=ds.__dict__[plot_var][::-1]
        lenY,lenX=data.shape

        print "-----------------------------------------------------"
        print plot_var
        print data

        ax=plt.subplot(111)
        plt.subplots_adjust(left=0.30,bottom=0.25)

        xx=np.arange(lenX) + 0.3
        width = 0.35

        yoff=np.array([0.]*xx)
        colours=self.get_colours(len(xx))
        pp=[]

        for h in range(lenY):
            yy=data[h,:]
            pp.append(plt.bar(xx, yy, width,
                    color=colours[h],bottom=yoff))
            yoff = yoff+yy

        #max_y is the height of the highest stacked bar
        max_y=1.1*np.ceil(max([self.dm[ti].__dict__[plot_var][:,vi][self.dm[ti].__dict__[plot_var][:,vi]>0].sum() for vi in range(lenX) for ti in range(self.sim.params.T_MAX)]))
        min_y=1.1*np.floor(min([self.dm[ti].__dict__[plot_var][:,vi][self.dm[ti].__dict__[plot_var][:,vi]<0].sum() for vi in range(lenX) for ti in range(self.sim.params.T_MAX)]))

        plt.xticks(xx+width/2.,np.arange(lenX))
        plt.ylim(min_y,max_y)
        #plt.yticks(np.arange(0,max_y*1.1+0.5,0.5))

        plt.ylabel(plot_var)
        plt.xlabel('vi')
        plt.title('Allocated {} per location'.format(plot_var))

        plt.axhline(y=0)

        legend_labels=["h="+str(x) for x in range(lenY)]
        legend_labels[0]=legend_labels[0]+":High income"
        legend_labels[-1]=legend_labels[-1]+":Low income"
        legend_labels=tuple(legend_labels)

        leg=plt.legend( tuple([x[0] for x in pp][::-1]),
                legend_labels, loc='best',fancybox=True)
        leg.get_frame().set_alpha(0.5)

        axcolor = 'lightgoldenrodyellow'
        axtime=plt.axes([0.25,0.1,0.65,0.03],axisbg=axcolor)
        axiter=plt.axes([0.25,0.15,0.65,0.03],axisbg=axcolor)

        radio_labels=['H_h_vi', 'I_h_vi','P_h_vi','b_h_vi','B_h_vi','avgZ_vi','H_h','b_h', 'r_vi', 'S_vi']
        rax = plt.axes([0.025, 0.4, 0.17, 0.05*len(radio_labels)], axisbg=axcolor)

        plt.title(self.sim.model_name+"-"+self.sim.data_name)
        stime = Slider(axtime, 'Time', 0, self.sim.params.T_MAX-1,valfmt='%1.0f', valinit=0)

        last_iter=max([self.dm[x].iters_count for x in range(self.sim.params.T_MAX)])
        iter=last_iter
        siter = Slider(axiter, 'Iter', 0, last_iter-1,valfmt='%1.0f', valinit=iter)

        radio = RadioButtons(rax,radio_labels , active=0)
        radio.val=radio_labels[0]
        bar_labels=self.autolabel(pp,ax)


        def update(val):
            t = int(round(stime.val,0))
            iter =int(round(siter.val,0))

            if val in radio_labels:
                radio.val=val
            plot_var=radio.val

            if iter<self.dm[t].iters_count:
                ds=self.dm[t].iters[iter]
            else:
                ds=self.dm[t]

            #TO DO: Permitir variables de dimension 1
            data=ds.__dict__[plot_var]
            if data.size>1:
                data=data[::-1]
                lenY,lenX=data.shape
            else:
                lenY=1
                lenX=1

            last_iter=self.dm[t].iters_count

            max_y=1.1*np.ceil(max([self.dm[ti].__dict__[plot_var][:,vi][self.dm[ti].__dict__[plot_var][:,vi]>0].sum() for vi in range(lenX) for ti in range(self.sim.params.T_MAX)]))
            min_y=1.1*np.floor(min([self.dm[ti].__dict__[plot_var][:,vi][self.dm[ti].__dict__[plot_var][:,vi]<0].sum() for vi in range(lenX) for ti in range(self.sim.params.T_MAX)]))

            plt.ylim(min_y,max_y)

            print "-----------------------------------------------------"
            print plot_var
            print data
            #plt.yticks(np.arange(0,max_y*1.1+0.5,0.5))
            plt.title('Allocated {} per location'.format(plot_var))
            plt.xlabel('vi')

            plt.axhline(y=0)

            yoff_pos=np.array([0.]*xx)
            yoff_neg=np.array([0.]*xx)
            for h in range(self.N_h):
                for vi in range(self.N_vi):
                    rect=pp[h][vi]
                    tt=bar_labels[h][vi]

                    if h < lenY and vi < lenX:
                        #update heights
                        height=data[h,vi]
                        rect.set_height(height)
                        if height>0:
                            rect.set_y(yoff_pos[vi])
                            yoff_pos[vi]+=height
                        else:
                            rect.set_y(yoff_neg[vi])
                            yoff_neg[vi]+=height

                        #update bar labels
                        tt.set_text("{:.2f}".format(height))
                        (bottom,top)=ax.get_ylim()
                        text_spot=rect.get_y()+height/2.
                        if bottom<text_spot<top:
                            tt.set_y(text_spot)

                        tt.set_visible(True)
                        rect.set_visible(True)
                    else:
                        tt.set_visible(False)
                        rect.set_visible(False)

            if lenY!=self.N_h:
                leg.set_visible(False)
            else:
                leg.set_visible(True)

            if lenX!=self.N_vi:
                plt.xlabel('')
            else:
                plt.xlabel('vi')

            plt.draw()

        stime.on_changed(update)
        siter.on_changed(update)
        radio.on_clicked(update)

        plt.show()


    def autolabel(self,pp,ax):
        plt.axes(ax)

        bar_labels=[]
        list_p=[]
        for h in range(len(pp)):
            for vi in range(self.N_vi):
                rect=pp[h][vi]
                height = rect.get_height()
                tt=plt.text(rect.get_x()+rect.get_width()/2., rect.get_y()+height/2., "{:.2f}".format(height),ha='center', va='center',axes=ax)
                list_p.append(tt)
            bar_labels.append(list_p)
            list_p=[]

        return bar_labels

    def pastel(self, colour, weight=2.4):
        """ Convert colour into a nice pastel shade"""
        rgb = np.asarray(colorConverter.to_rgb(colour))
        # scale colour
        maxc = max(rgb)
        if maxc < 1.0 and maxc > 0:
            # scale colour
            scale = 1.0 / maxc
            rgb = rgb * scale
        # now decrease saturation
        total = sum(rgb)
        slack = 0
        for x in rgb:
            slack += 1.0 - x

        # want to increase weight from total to weight
        # pick x s.t.  slack * x == weight - total
        # x = (weight - total) / slack
        x = (weight - total) / slack

        rgb = [c + (x * (1.0-c)) for c in rgb]

        return rgb

    def get_colours(self,n):
        """ Return n pastel colours. """
        base = np.asarray([[1,0,0], [0,1,0], [0,0,1]])

        if n <= 3:
            return base[0:n]

        # how many new colours to we need to insert between
        # red and green and between green and blue?
        needed = (((n - 3) + 1) / 2, (n - 3) / 2)

        colours = []
        for start in (0, 1):
            for x in np.linspace(0, 1, needed[start]+2):
                colours.append((base[start] * (1.0 - x)) +
                               (base[start+1] * x))

        return [self.pastel(c) for c in colours[0:n]]

